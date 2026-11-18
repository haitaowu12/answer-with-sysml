#!/usr/bin/env python3
"""Compile a reviewed architecture recipe to editable SysML v2, never to test results.

This bounded authoring adapter does not read prose or infer responsibilities. Its
input records are engineering proposals. The language engine and the separate
architecture checker must reconcile the output before native validation is claimed.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re


COLLECTIONS = ('actors', 'operationalActivities', 'functions', 'exchanges',
               'logicalComponents', 'allocations', 'scenarios', 'requirements',
               'verificationCases', 'decisions', 'stateMachines', 'insights', 'contextExchanges')

# Identifier keywords from the locked 2025-09 Pilot's InternalSysML.tokens.
# Its token-file SHA256 is 22374bc6194311e03d3de294df7ccaab7d5bd42c9aa33f230d419ede7ff0dc96.
# Also protect the implicit behavior endpoints start/done from accidental reuse.
RESERVED = frozenset('''about abstract accept action actor after alias all allocate allocation
analysis and as assert assign assume at attribute bind binding by calc case comment concern
connect connection constant constraint crosses decide def default defined dependency derived
do doc done else end entry enum event exhibit exit expose false filter first flow for fork frame
from hastype if implies import in include individual inout interface istype item join language
library locale loop merge message meta metadata new nonunique not null objective occurrence of
or ordered out package parallel part perform port private protected public redefines ref
references render rendering rep require requirement return satisfy send snapshot specializes
stakeholder standard start state subject subsets succession terminate then timeslice to
transition true until use variant variation verification verify via view viewpoint when while xor'''.split())


def ident(value):
    """Stable escaping with collision rejection in Emitter, not silently lossy IDs."""
    name = re.sub(r'[^A-Za-z0-9_]', '_', str(value))
    return 'n_' + name if not name or name[0].isdigit() or name in RESERVED else name


def display_name(label):
    label = ' '.join(label.replace('\x00', '').split())
    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', label) and label not in RESERVED:
        return label
    return "'" + label.replace("\\", "\\\\").replace("'", "\\'") + "'"


def comment(value):
    return str(value).replace('*/', '* /').replace('\x00', '')


def document(record, extra=()):
    lines = [record.get('label', record.get('id', '')), record.get('description', '')]
    lines += ['Record: ' + record['id']] if record.get('id') else []
    lines += ['Basis: ' + record.get('basis', 'proposed') + '; status: ' + record.get('status', 'draft') + '.']
    lines += ['Source: ' + s for s in record.get('sourceRefs', [])]
    if record.get('acceptanceEvidence'):
        lines += ['Acceptance evidence: ' + json.dumps(record['acceptanceEvidence'], ensure_ascii=False, sort_keys=True)]
    lines += [str(x) for x in extra if x]
    return 'doc /* ' + comment('\n'.join(x for x in lines if x)) + ' */'


class Emitter:
    def __init__(self, packet, package='ConOpsArchitecture'):
        self.packet = packet
        self.package = ident(package)
        self.records = {r['id']: r for k in COLLECTIONS for r in packet.get(k, [])}
        self.names = {i: ident(i) for i in self.records}
        if len(set(self.names.values())) != len(self.names):
            raise ValueError('IDs collide after native name escaping')
        if len(self.records) != sum(len(packet.get(k, [])) for k in COLLECTIONS):
            raise ValueError('Architecture IDs must be globally unique')
        self.lines, self.depth = [], 0
        self.bindings = {'schemaVersion': 1, 'elements': {}, 'expected': {'schemaVersion': 1, 'checks': []}, 'coverage': {}, 'interfaces': {}, 'realizations': [], 'parallelGroups': {}}
        self.paths, self.expressions, self.types = {}, {}, {}
        self.children = {}
        for key, section, root in [('functions', 'System', 'functions'), ('operationalActivities', 'Operational', 'activities'), ('logicalComponents', 'Logical', 'architecture')]:
            records = packet.get(key, [])
            ids = {r['id'] for r in records}
            self.children[key] = defaultdict(list)
            for r in records:
                if r.get('parent') and r['parent'] not in ids:
                    raise ValueError('Unknown hierarchy parent: ' + r['id'])
                self.children[key][r.get('parent')].append(r)
            def visit(parent, chain, seen):
                for r in self.children[key].get(parent, []):
                    if r['id'] in seen:
                        raise ValueError('Cyclic architecture hierarchy')
                    names = chain + [self.names[r['id']]]
                    self.paths[r['id']] = [self.package + '::' + section + '::' + '::'.join(names[:i+1]) for i in range(len(names))]
                    self.expressions[r['id']] = section + '::' + '.'.join(names)
                    self.types[r['id']] = self.package + '::Types::T_' + self.names[r['id']]
                    visit(r['id'], names, seen | {r['id']})
            visit(None, [root], set())
            if any(r['id'] not in self.paths for r in records):
                raise ValueError('Unreachable or cyclic hierarchy')
        for r in packet.get('actors', []):
            self.paths[r['id']] = [self.package + '::Operational::context', self.package + '::Operational::context::' + self.names[r['id']]]
            self.expressions[r['id']] = 'Operational::context.' + self.names[r['id']]
            self.types[r['id']] = self.package + '::Types::T_' + self.names[r['id']]
        self.allocations = {a['function']: a['component'] for a in packet.get('allocations', [])}
        if len(self.allocations) != len(packet.get('allocations', [])):
            raise ValueError('This authoring profile requires one primary logical allocation per function; model alternatives as separate configurations')
        self.cross = []
        for x in packet.get('exchanges', []):
            a, b = self.allocations.get(x['source']), self.allocations.get(x['target'])
            if a and b and a != b:
                self.cross.append((x, a, b))
        self.boundary_contracts = [(x, x['source'], x['target']) for x in packet.get('contextExchanges', [])]
        part_ids = {r['id'] for k in ('actors', 'logicalComponents') for r in packet.get(k, [])}
        if any(a not in part_ids or b not in part_ids for _, a, b in self.boundary_contracts):
            raise ValueError('A context contract must connect declared actor/logical responsibility occurrences')
        self.contracts = self.cross + self.boundary_contracts

    def line(self, value=''):
        for text in value.split('\n'):
            self.lines.append('    ' * self.depth + text)

    def begin(self, value):
        self.line(value + ' {'); self.depth += 1

    def end(self):
        self.depth -= 1; self.line('}')

    def check(self, cid, name, metaclass, expect=None, record=None):
        c = {'id': cid, 'select': {'qualifiedName': name, 'metaclass': metaclass}, 'candidateCount': 1, 'expect': expect or {'metaclass': metaclass}}
        self.bindings['expected']['checks'].append(c)
        if record:
            self.bindings['coverage'].setdefault(record, []).append(cid)

    def bind(self, rid, qn, metaclass, expect=None, **extra):
        self.bindings['elements'][rid] = dict(qualifiedName=qn, metaclass=metaclass, **extra)
        self.check('element:' + rid, qn, metaclass, expect, rid)

    def emit_types(self):
        self.begin('package Types')
        for x in self.packet.get('exchanges', []) + self.packet.get('contextExchanges', []):
            self.begin('item def I_' + self.names[x['id']])
            self.line(document(x, [x.get('item', ''), 'Potential exchange; applicability: ' + x.get('condition', '')]))
            self.end()
        for r in self.packet.get('actors', []):
            self.begin('part def T_' + self.names[r['id']]); self.line(document(r))
            for x, a, b in self.boundary_contracts:
                if r['id'] in (a, b):
                    xn = self.names[x['id']]
                    self.line('port p_' + xn + ' : ' + ('~' if r['id'] == b else '') + 'P_' + xn + ';')
            self.end()
        for key in ('operationalActivities', 'functions', 'logicalComponents'):
            for r in self.packet.get(key, []):
                typ = 'part' if key == 'logicalComponents' else 'action'
                self.begin(typ + ' def T_' + self.names[r['id']]); self.line(document(r))
                if key == 'functions':
                    for x in self.packet.get('exchanges', []):
                        xn = self.names[x['id']]
                        if x['source'] == r['id']:
                            self.line('out item out_' + xn + ' : I_' + xn + ';')
                        if x['target'] == r['id']:
                            self.line('in item in_' + xn + ' : I_' + xn + ';')
                if key == 'logicalComponents':
                    for x, a, b in self.contracts:
                        if r['id'] in (a, b):
                            xn = self.names[x['id']]
                            self.line('port p_' + xn + ' : ' + ('~' if r['id'] == b else '') + 'P_' + xn + ';')
                attrs = {}
                for req in self.packet.get('requirements', []):
                    c = req.get('formalConstraint')
                    if c and req['subject'] == r['id']:
                        name = ident(c['attribute'])
                        dtype = 'ISQBase::DurationValue' if c['quantity'] == 'duration' else 'Real'
                        if name in attrs and attrs[name] != dtype:
                            raise ValueError('Conflicting formal subject attribute types')
                        attrs[name] = dtype
                for name, dtype in attrs.items():
                    self.line('attribute ' + name + ' : ' + dtype + ';')
                self.end()
        for x, _, _ in self.contracts:
            xn = self.names[x['id']]
            self.begin('port def P_' + xn); self.line('out item payload : I_' + xn + ';'); self.end()
            self.begin('interface def IF_' + xn)
            self.line('end sender : P_' + xn + ';'); self.line('end receiver : ~P_' + xn + ';')
            self.line('flow of I_' + xn + ' from sender.payload to receiver.payload;'); self.end()
        for s in self.packet.get('stateMachines', []):
            for t in s.get('transitions', []):
                if t.get('event'):
                    self.begin('item def Event_' + ident(s['id'] + '_' + t['id']))
                    self.line('doc /* ' + comment(t['event']) + ' */'); self.end()
            self.begin('state def T_' + self.names[s['id']])
            self.line(document(s, ['Lifecycle policy: ' + s.get('terminalPolicy', 'finite when terminal states are declared'),
                'Terminal states: ' + ', '.join(s.get('terminalStates', [])),
                'Lifecycle exit condition: ' + s.get('lifecycleExitCondition', ''),
                'Transition effects below are retained obligations, not executed effects.']))
            states = s['states']; initial = s.get('initial', states[0]['id'])
            self.line('entry;'); self.line('then ' + ident(initial) + ';')
            for st in states:
                self.begin('state ' + ident(st['id'])); self.line('doc /* ' + comment(st.get('label', st['id'])) + ' */'); self.end()
            for t in s.get('transitions', []):
                tn = ident(t['id'])
                if t.get('guard'):
                    self.begin('attribute g_' + tn + ' : Boolean')
                    self.line('doc /* Review predicate, not an evaluated value: ' + comment(t['guard']) + ' */'); self.end()
                transition = 'transition ' + tn + ' first ' + ident(t['from'])
                if t.get('event'):
                    transition += ' accept Event_' + ident(s['id'] + '_' + t['id'])
                if t.get('guard'):
                    transition += ' if g_' + tn
                transition += ' then ' + ident(t['to'])
                self.begin(transition); self.line('doc /* Effect/obligation: ' + comment(t.get('effect', '')) + ' */'); self.end()
            for terminal in s.get('terminalStates', []):
                if terminal not in {st['id'] for st in states}:
                    raise ValueError('Unknown terminal state: ' + terminal)
                self.line('transition finish_' + ident(terminal) + ' first ' + ident(terminal) + ' then done;')
            self.end()
        self.end()

    def hierarchy(self, key, parent=None):
        for r in self.children[key].get(parent, []):
            name, qn = self.names[r['id']], self.paths[r['id']][-1]
            kind = 'part' if key == 'logicalComponents' else 'action'
            mc = 'PartUsage' if kind == 'part' else 'ActionUsage'
            self.begin(kind + ' ' + name + ' : Types::T_' + name)
            self.line(document(r))
            self.bind(r['id'], qn, mc, {'typeIncludes': self.types[r['id']]})
            self.hierarchy(key, r['id'])
            for sm in self.packet.get('stateMachines', []):
                if sm.get('subject') == r['id']:
                    sn = self.names[sm['id']]
                    self.line('exhibit state ' + sn + ' : Types::T_' + sn + ';')
                    definition = self.package + '::Types::T_' + sn
                    self.bind(sm['id'], qn + '::' + sn, 'ExhibitStateUsage', {'typeIncludes': definition},
                              definition=definition, subjectId=r['id'],
                              states={st['id']: definition + '::' + ident(st['id']) for st in sm['states']},
                              transitions={t['id']: definition + '::' + ident(t['id']) for t in sm['transitions']},
                              terminalTransitions={st: definition + '::finish_' + ident(st) for st in sm.get('terminalStates', [])},
                              initial=definition + '::' + ident(sm.get('initial', sm['states'][0]['id'])))
            self.end()

    def emit_operational(self):
        self.begin('package Operational')
        self.begin('action activities'); self.hierarchy('operationalActivities'); self.end()
        self.begin('part context')
        for r in self.packet.get('actors', []):
            rn = self.names[r['id']]
            self.begin('ref part ' + rn + ' : Types::T_' + rn); self.line(document(r))
            self.bind(r['id'], self.paths[r['id']][-1], 'PartUsage', {'typeIncludes': self.types[r['id']]})
            for a in self.packet.get('operationalActivities', []):
                if a.get('performer') == r['id']:
                    self.line('perform ' + self.expressions[a['id']].removeprefix('Operational::') + ';')
                    self.bindings['expected']['checks'].append({'id': 'perform:' + a['id'], 'select': {'owner': self.paths[r['id']][-1], 'metaclass': 'PerformActionUsage'}, 'expect': {'references': {'performedAction': self.paths[a['id']][-1]}}, 'count': 1})
                    self.bindings['coverage'].setdefault(a['id'], []).append('perform:' + a['id'])
            self.end()
        self.end(); self.end()

    def emit_system(self):
        self.begin('package System'); self.begin('action functions'); self.hierarchy('functions'); self.end()
        for x in self.packet.get('exchanges', []):
            xn = self.names[x['id']]
            source = self.expressions[x['source']].removeprefix('System::') + '.out_' + xn
            target = self.expressions[x['target']].removeprefix('System::') + '.in_' + xn
            self.begin('flow ' + xn + ' of Types::I_' + xn + ' from ' + source + ' to ' + target)
            self.line(document(x, ['Applicability: ' + x.get('condition', '')])); self.end()
            self.bind(x['id'], self.package + '::System::' + xn, 'FlowUsage',
                      {'source': self.paths[x['source']], 'targets': [self.paths[x['target']]]},
                      sourceId=x['source'], targetId=x['target'],
                      sourceOutput=self.types[x['source']] + '::out_' + xn,
                      targetInput=self.types[x['target']] + '::in_' + xn)
        self.end()

    def emit_logical(self):
        self.begin('package Logical'); self.begin('part architecture'); self.hierarchy('logicalComponents'); self.end()
        for x, a, b in self.cross:
            xn = self.names[x['id']]
            self.begin('interface IF_' + xn + ' : Types::IF_' + xn + ' connect ' + self.expressions[a].removeprefix('Logical::') + '.p_' + xn + ' to ' + self.expressions[b].removeprefix('Logical::') + '.p_' + xn)
            self.line(document(x, ['Derived logical contract from candidate primary function allocations.'])); self.end()
            self.check('interface:' + x['id'], self.package + '::Logical::IF_' + xn, 'InterfaceUsage', {'typeIncludes': self.package + '::Types::IF_' + xn}, x['id'])
            self.bindings['interfaces'][x['id']] = {
                'qualifiedName': self.package + '::Logical::IF_' + xn,
                'sourceComponentId': a, 'targetComponentId': b,
                'sourcePort': self.types[a] + '::p_' + xn,
                'targetPort': self.types[b] + '::p_' + xn,
                'payloadType': self.package + '::Types::I_' + xn,
            }
        self.end()
        for a in self.packet.get('allocations', []):
            self.begin('allocation ' + self.names[a['id']] + ' allocate ' + self.expressions[a['function']] + ' to ' + self.expressions[a['component']])
            self.line(document(a, [a.get('rationale', '')])); self.end()
            self.bind(a['id'], self.package + '::' + self.names[a['id']], 'AllocationUsage',
                      {'source': self.paths[a['function']], 'targets': [self.paths[a['component']]]},
                      sourceId=a['function'], targetId=a['component'])
        for f in self.packet.get('functions', []):
            for activity in f.get('realizes', []):
                if activity not in self.paths:
                    raise ValueError('Unknown operational activity realized by ' + f['id'])
                self.begin('dependency trace_' + self.names[f['id']] + '_' + self.names[activity] + ' from ' + self.paths[f['id']][-1] + ' to ' + self.paths[activity][-1])
                self.line('doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */'); self.end()
                self.bindings['realizations'].append({'functionId': f['id'], 'activityId': activity,
                    'qualifiedName': self.package + '::trace_' + self.names[f['id']] + '_' + self.names[activity]})

    def emit_context_contracts(self):
        self.begin('package Context')
        for x, a, b in self.boundary_contracts:
            xn = self.names[x['id']]
            self.begin('interface ' + xn + ' : Types::IF_' + xn + ' connect ' +
                       self.expressions[a] + '.p_' + xn + ' to ' + self.expressions[b] + '.p_' + xn)
            self.line(document(x, ['Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority.']))
            self.end()
            self.bind(x['id'], self.package + '::Context::' + xn, 'InterfaceUsage',
                      {'typeIncludes': self.package + '::Types::IF_' + xn},
                      sourceId=a, targetId=b, sourcePort=self.types[a] + '::p_' + xn,
                      targetPort=self.types[b] + '::p_' + xn,
                      payloadType=self.package + '::Types::I_' + xn)
        self.end()

    def emit_scenarios(self):
        self.begin('package Scenarios')
        for s in self.packet.get('scenarios', []):
            sn = self.names[s['id']]; qn = self.package + '::Scenarios::' + sn
            self.begin('action ' + sn)
            self.line(document(s, ['Entry: ' + '; '.join(s.get('entryConditions', [])), 'Exit: ' + '; '.join(s.get('exitConditions', [])), 'Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed.']))
            self.bind(s['id'], qn, 'ActionUsage')
            steps = {x['id']: x for x in s['steps']}
            if len(steps) != len(s['steps']) or len({ident(i) for i in steps}) != len(steps):
                raise ValueError('Scenario step IDs must be unique after native escaping: ' + s['id'])
            names = set(ident(t['id']) for t in s.get('transitions', [])) | {'start', 'done', 'ActionFlow'}
            for group in s.get('parallelGroups', []):
                names.update('control_' + ident(group['id']) + '_' + suffix
                             for suffix in ('fork', 'join', 'enter', 'leave'))

            def readable_name(label, record_id):
                name = display_name(label)
                if name in names:
                    name = display_name(f'{label} ({record_id})')
                if name in names:
                    raise ValueError('Scenario labels collide: ' + record_id)
                names.add(name)
                return name

            step_names = {st['id']: readable_name(st.get('label') or self.records[st['function']]['label'], st['id'])
                          for st in s['steps']}
            for st in s['steps']:
                self.begin('action ' + step_names[st['id']] + ' : Types::T_' + self.names[st['function']])
                self.line('doc /* ' + comment(st.get('label') or self.records[st['function']]['label']) + ' (Record: ' + comment(st['id']) + ')' + '; responsible role: ' + comment(st.get('actor', 'unresolved')) + ' */'); self.end()
                rid = s['id'] + '/' + st['id']
                self.bind(rid, qn + '::' + step_names[st['id']], 'ActionUsage', {'typeIncludes': self.types[st['function']]}, functionId=st['function'])
            entry = s.get('entryStep', s['steps'][0]['id'])
            self.line('first start then ' + step_names[entry] + ';')
            control_ends = {}
            for group in s.get('parallelGroups', []):
                gid = group['id']; gn = 'control_' + ident(gid)
                fork, join = gn + '_fork', gn + '_join'
                branch_links = [t for t in s.get('transitions', []) if t['from'] == group['from'] and t['to'] in group['branches'] and t.get('kind') == 'parallel']
                join_links = [t for t in s.get('transitions', []) if t['to'] == group.get('join') and t.get('kind') == 'join']
                if (group['from'] not in steps or group.get('join') not in steps or
                        set(group['branches']) != {t['to'] for t in branch_links} or
                        len(branch_links) != len(group['branches']) or len(join_links) != len(group['branches'])):
                    raise ValueError('Parallel group requires explicit branch and joining transitions: ' + gid)
                # This profile has one completion contribution per obligation.
                # Alternatives must merge before joining; otherwise a native
                # join would wait for mutually exclusive outcomes simultaneously.
                adjacency = defaultdict(set)
                for link in s.get('transitions', []):
                    if link['from'] != group['join'] and link['to'] != group['join']:
                        adjacency[link['from']].add(link['to'])
                completions = []
                for branch in group['branches']:
                    reachable, pending = set(), [branch]
                    while pending:
                        node = pending.pop()
                        if node in reachable:
                            continue
                        reachable.add(node); pending.extend(adjacency[node])
                    matches = [t['id'] for t in join_links if t['from'] in reachable]
                    if len(matches) != 1:
                        raise ValueError('Parallel alternatives must merge before the join: ' + gid + '/' + branch)
                    completions.extend(matches)
                if len(set(completions)) != len(group['branches']):
                    raise ValueError('Concurrent branches need distinct completion contributions: ' + gid)
                self.line('fork ' + fork + ';')
                self.line('join ' + join + ';')
                self.line('succession ' + gn + '_enter first ' + step_names[group['from']] + ' then ' + fork + ';')
                self.line('succession ' + gn + '_leave first ' + join + ' then ' + step_names[group['join']] + ';')
                self.bind(s['id'] + '/' + gid + '/fork', qn + '::' + fork, 'ForkNode')
                self.bind(s['id'] + '/' + gid + '/join', qn + '::' + join, 'JoinNode')
                for name, source, target in [(gn + '_enter', step_names[group['from']], fork), (gn + '_leave', join, step_names[group['join']])]:
                    self.check('control:' + s['id'] + '/' + name, qn + '::' + name, 'SuccessionAsUsage',
                               {'source': [qn + '::' + source], 'targets': [[qn + '::' + target]]})
                for t in branch_links:
                    if t['id'] in control_ends:
                        raise ValueError('Overlapping parallel groups: ' + t['id'])
                    control_ends[t['id']] = (fork, step_names[t['to']])
                for t in join_links:
                    if t['id'] in control_ends:
                        raise ValueError('Overlapping parallel groups: ' + t['id'])
                    control_ends[t['id']] = (step_names[t['from']], join)
                self.bindings['parallelGroups'][s['id'] + '/' + gid] = {
                    'scenarioId': s['id'], 'fork': qn + '::' + fork, 'join': qn + '::' + join,
                    'fromId': group['from'], 'branchIds': group['branches'], 'joinStepId': group['join'],
                    'branchTransitionIds': [t['id'] for t in branch_links],
                    'joinTransitionIds': [t['id'] for t in join_links],
                    'entryLink': qn + '::' + gn + '_enter', 'exitLink': qn + '::' + gn + '_leave'}
            outgoing = set()
            for t in s.get('transitions', []):
                if t['from'] not in steps or t['to'] not in steps:
                    raise ValueError('Scenario transition requires existing step endpoints: ' + t['id'])
                outgoing.add(t['from']); tn = ident(t['id'])
                if t.get('condition'):
                    guard_name = readable_name(t['condition'], t['id'])
                    self.begin('attribute ' + guard_name + ' : Boolean')
                    self.line('doc /* Review predicate: ' + comment(t['condition']) + ' */'); self.end()
                if t.get('kind') in ('parallel', 'join') and t['id'] not in control_ends:
                    raise ValueError('Parallel/join transition lacks a declared control group: ' + t['id'])
                source, target = control_ends.get(t['id'], (step_names[t['from']], step_names[t['to']]))
                declaration = 'succession ' + tn + ' first ' + source
                if t.get('condition'): declaration += ' if ' + guard_name
                self.begin(declaration + ' then ' + target)
                self.line('doc /* ' + comment(t.get('condition', '')) + '; outcome: ' + comment(t.get('outcome', '')) + ' */'); self.end()
                mc = 'TransitionUsage' if t.get('condition') else 'SuccessionAsUsage'
                expectation = ({'references': {'source': qn + '::' + source, 'target': qn + '::' + target, 'guardExpression': qn + '::' + tn + '::guard'}}
                               if t.get('condition') else {'source': [qn + '::' + source], 'targets': [[qn + '::' + target]]})
                self.bind(t['id'], qn + '::' + tn, mc,
                          expectation,
                          scenarioId=s['id'], fromId=t['from'], toId=t['to'],
                          nativeSource=qn + '::' + source, nativeTarget=qn + '::' + target)
            # End declarations express completion of the documented fragment.
            # Cyclic fragments retain only their explicit exit criteria in prose.
            for step in sorted(set(s.get('exitSteps', steps.keys() - outgoing))):
                if step not in steps:
                    raise ValueError('Unknown scenario completion step: ' + step)
                guard = s.get('exitGuards', {}).get(step)
                if guard:
                    gn = readable_name(guard, 'completion ' + step)
                    self.begin('attribute ' + gn + ' : Boolean')
                    self.line('doc /* Completion criterion: ' + comment(guard) + ' */'); self.end()
                    self.line('first ' + step_names[step] + ' if ' + gn + ' then done;')
                else:
                    self.line('first ' + step_names[step] + ' then done;')
            self.emit_view('ActionFlow', qn, 'ActionFlowView', [sn + '::*'], s.get('label', s['id']))
            self.end()
        self.end()

    def emit_requirements(self):
        self.begin('package Requirements')
        requirement_names = {}
        for r in self.packet.get('requirements', []):
            rn = display_name(r.get('label') or r['id'])
            if rn in requirement_names.values():
                rn = display_name(f'{r["label"]} ({r["id"]})')
            if rn in requirement_names.values():
                raise ValueError('Requirement names collide: ' + r['id'])
            requirement_names[r['id']] = rn
            qn = self.package + '::Requirements::' + rn
            subj = r['subject']
            self.begin('requirement <' + display_name(r['id']) + '> ' + rn)
            statement = r.get('statement') or ' '.join(
                text for text in ('Applicability: ' + r['condition'] if r.get('condition') else '',
                                  r.get('criterion', '')) if text)
            self.line('doc /* ' + comment(statement) + ' */')
            note = [f'Basis: {r.get("basis", "proposed")}; status: {r.get("status", "draft")}.']
            note.extend('Source: ' + source for source in r.get('sourceRefs', []))
            if r.get('rationale'):
                note.append('Rationale: ' + r['rationale'])
            if r.get('acceptanceEvidence'):
                note.append('Acceptance evidence: ' + json.dumps(r['acceptanceEvidence'], ensure_ascii=False, sort_keys=True))
            self.line('comment ReviewBasis /* ' + comment('\n'.join(note)) + ' */')
            self.line('subject subjectOfRequirement : ' + self.types[subj] + ' = ' + self.expressions[subj] + ';')
            self.begin('require constraint criterion')
            c = r.get('formalConstraint')
            if c:
                if c.get('operator') not in ('>=', '<=', '==', '>', '<') or c.get('quantity') not in ('duration', 'number') or type(c.get('value')) not in (int, float):
                    raise ValueError('Unsupported formal constraint shape')
                if c['quantity'] == 'duration' and c.get('unit') not in ('s', 'min', 'h', 'd'):
                    raise ValueError('Unsupported duration unit')
                suffix = ' [SI::' + c['unit'] + ']' if c['quantity'] == 'duration' else ''
                self.line('subjectOfRequirement.' + ident(c['attribute']) + ' ' + c['operator'] + ' ' + str(c['value']) + suffix)
            else:
                self.line('doc /* ' + comment(r.get('criterion', 'Unresolved criterion')) + ' */')
            self.end(); self.end()
            extra = {'formalAttribute': self.types[subj] + '::' + ident(c['attribute'])} if c else {}
            self.bind(r['id'], qn, 'RequirementUsage', {'references': {'subjectParameter': qn + '::subjectOfRequirement', 'requiredConstraint': qn + '::criterion'}}, subjectId=subj, requirementId=r['id'], statement=statement, **extra)
            self.check('subject:' + r['id'], qn + '::subjectOfRequirement', 'ReferenceUsage', {'typeIncludes': self.types[subj]}, r['id'])
            self.check('criterion:' + r['id'], qn + '::criterion', 'ConstraintUsage', {'constraintKind': 'requirement'}, r['id'])
        self.end()
        self.begin('package Verification')
        reqs = {r['id']: r for r in self.packet.get('requirements', [])}
        for v in self.packet.get('verificationCases', []):
            vn = self.names[v['id']]; qn = self.package + '::Verification::' + vn
            if v.get('status') != 'planned':
                raise ValueError('This authoring profile emits planned verification only; executed results need separate evidence')
            if len({reqs[key]['subject'] for key in v['requirementIds']}) != 1:
                raise ValueError('A bounded verification definition requires one common subject; author a broader case explicitly for ' + v['id'])
            self.begin('verification def ' + vn)
            self.line(document(v, ['Method: ' + v.get('method', ''), 'Setup: ' + str(v.get('setup', '')), 'Expected result: ' + v.get('expectedResult', ''), 'No executed result or acceptance recorded.']))
            subject = reqs[v['requirementIds'][0]]['subject']
            self.line('subject subjectUnderReview : ' + self.types[subject] + ';')
            self.begin('objective')
            for req in v['requirementIds']:
                self.line('verify Requirements::' + requirement_names[req] + ';')
            self.end(); self.end()
            self.bind(v['id'], qn, 'VerificationCaseDefinition', {'references': {'verifiedRequirement': self.package + '::Requirements::' + requirement_names[v['requirementIds'][0]]}})
            for req in v['requirementIds']:
                self.check('verifies:' + v['id'] + ':' + req, qn, 'VerificationCaseDefinition', {'references': {'verifiedRequirement': self.package + '::Requirements::' + requirement_names[req]}}, v['id'])
        self.end()

    def emit_view(self, name, owner, kind, scope, question):
        view_type = 'StandardViewDefinitions::' + kind
        self.begin('view ' + name + ' : ' + view_type)
        self.line('doc /* ' + comment(question) + ' */')
        for member in scope:
            self.line('expose ' + member + ';')
        self.end()
        qn = owner + '::' + name
        self.check('view:' + qn, qn, 'ViewUsage', {'typeIncludes': view_type})

    def emit_review_views(self):
        self.begin('package ReviewViews')
        self.emit_view('OperationalContext', self.package + '::ReviewViews', 'GeneralView',
                       ['Operational::context::*', 'Operational::activities::*'],
                       'Who participates and what operational activities are in scope?')
        self.emit_view('SystemFunctions', self.package + '::ReviewViews', 'GeneralView',
                       ['System::functions::*'],
                       'How is the system function decomposed?')
        self.emit_view('LogicalInterfaces', self.package + '::ReviewViews', 'InterconnectionView',
                       ['Logical::architecture::*', 'Logical::*'],
                       'Which proposed responsibilities exchange information or material?')
        if self.packet.get('requirements'):
            self.emit_view('RequirementsAndVerification', self.package + '::ReviewViews', 'GeneralView',
                           ['Requirements::*', 'Verification::*'],
                           'What must hold and what verification is planned?')
        for sm in self.packet.get('stateMachines', []):
            self.emit_view('Lifecycle_' + self.names[sm['id']], self.package + '::ReviewViews', 'StateTransitionView',
                           ['Types::T_' + self.names[sm['id']] + '::*'],
                           sm.get('label', sm['id']))
        self.end()

    def emit(self):
        self.begin('package ' + self.package)
        self.line('private import ScalarValues::*;')
        self.line(document({'label': self.packet.get('scope', {}).get('name', 'Architecture study'), 'description': self.packet.get('scope', {}).get('boundary', ''), 'basis': 'proposed', 'status': 'draft'}, ['Concept architecture for review. Source statements, derived mappings and design proposals retain separate status.']))
        self.emit_types(); self.emit_operational(); self.emit_system(); self.emit_logical(); self.emit_context_contracts(); self.emit_scenarios(); self.emit_requirements(); self.emit_review_views()
        self.begin('package ReviewDecisions')
        for d in self.packet.get('decisions', []):
            self.begin('package ' + self.names[d['id']]); self.line(document(d, [d.get('question', ''), 'Alternatives: ' + json.dumps(d.get('options', []), ensure_ascii=False)])); self.end()
            self.bind(d['id'], self.package + '::ReviewDecisions::' + self.names[d['id']], 'Package')
        self.end(); self.end()
        source = '\n'.join(self.lines) + '\n'
        self.bindings['modelSha256'] = hashlib.sha256(source.encode()).hexdigest()
        self.bindings['boundary'] = 'Generated reconciliation expectations check recipe-to-language translation. They are not independent source-meaning acceptance or executed verification.'
        self.bindings['recipeSha256'] = hashlib.sha256(json.dumps(self.packet, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        return source, self.bindings


def build(packet, output, package='ConOpsArchitecture'):
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new output directory; preserve the previous architecture package')
    source, bindings = Emitter(packet, package).emit()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'model.sysml').write_text(source, encoding='utf-8')
    (output / 'architecture.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'bindings.json').write_text(json.dumps(bindings, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'translation-checks.json').write_text(json.dumps(bindings['expected'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'output': str(output), 'modelSha256': bindings['modelSha256'], 'boundRecords': len(bindings['elements']), 'languageValidation': 'not-run'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--architecture', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--package', default='ConOpsArchitecture')
    a = p.parse_args()
    print(json.dumps(build(json.loads(a.architecture.read_text()), a.output, a.package), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
