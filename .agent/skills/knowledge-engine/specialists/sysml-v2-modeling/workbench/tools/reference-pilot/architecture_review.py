#!/usr/bin/env python3
"""Build one portable, question-led reader from an explicit architecture recipe.

This is a communication projection of authored architecture and checked native
bindings. It does not infer topology from prose, execute behavior, or accept a
design. The complete source inventory is available once, behind search.
"""
import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import textwrap
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
COLLECTIONS = {
    'actors': 'Operational participant', 'operationalActivities': 'Operational activity',
    'functions': 'System function', 'exchanges': 'Functional exchange',
    'logicalComponents': 'Logical responsibility', 'allocations': 'Function allocation',
    'scenarios': 'Scenario', 'requirements': 'Candidate requirement',
    'verificationCases': 'Planned verification', 'decisions': 'Open decision',
    'stateMachines': 'Lifecycle', 'insights': 'Architecture insight',
    'contextExchanges': 'Boundary contract', 'parameters': 'Parameter',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def recipe_digest(packet):
    return digest(json.dumps(packet, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode())


def encoded(value):
    """JSON data inside an inert script element, including hostile source text."""
    return (json.dumps(value, ensure_ascii=False, separators=(',', ':'))
            .replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
            .replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))


def record_index(packet, bindings):
    records = {}
    for collection, category in COLLECTIONS.items():
        for item in packet.get(collection, []):
            if item['id'] in records:
                raise ValueError('Architecture IDs must be unique: ' + item['id'])
            records[item['id']] = dict(deepcopy(item), collection=collection, category=category)
    for scenario in packet.get('scenarios', []):
        for step in scenario.get('steps', []):
            key = scenario['id'] + '/' + step['id']
            records[key] = dict(deepcopy(step), id=key, localId=step['id'],
                                scenario=scenario['id'], collection='scenarioSteps', category='Scenario step',
                                sourceRefs=scenario.get('sourceRefs', []), basis=scenario.get('basis'), status=scenario.get('status'))
            if step['id'] in scenario.get('exitGuards', {}):
                records[key]['exitGuard'] = scenario['exitGuards'][step['id']]
        for transition in scenario.get('transitions', []):
            records[transition['id']] = dict(deepcopy(transition), scenario=scenario['id'],
                source=scenario['id'] + '/' + transition['from'], target=scenario['id'] + '/' + transition['to'],
                label=transition.get('condition') or transition.get('outcome') or 'Declared succession',
                collection='scenarioTransitions', category='Guarded scenario transition',
                sourceRefs=scenario.get('sourceRefs', []), basis=scenario.get('basis'), status=scenario.get('status'))
        for group in scenario.get('parallelGroups', []):
            prefix = scenario['id'] + '/' + group['id']
            binding = bindings.get('parallelGroups', {}).get(prefix, {})
            records[prefix] = dict(deepcopy(group), id=prefix, label='Concurrent obligations',
                scenario=scenario['id'], collection='scenarioConcurrency', category='Concurrency group',
                sourceRefs=scenario.get('sourceRefs', []), basis=scenario.get('basis'), status=scenario.get('status'))
            for field, title, kind in [('fork', 'Fork · both obligations', 'ForkNode'), ('join', 'Join · both contributions', 'JoinNode'),
                                       ('entryLink', 'Enter concurrent obligations', 'SuccessionAsUsage'), ('exitLink', 'Continue after both contributions', 'SuccessionAsUsage')]:
                key = prefix + '/' + field
                records[key] = dict(id=key, label=title, description=group.get('description', ''),
                    scenario=scenario['id'], relatedIds=[prefix], collection='scenarioControls', category='Concurrency control',
                    sourceRefs=scenario.get('sourceRefs', []), basis=scenario.get('basis'), status=scenario.get('status'))
                if binding.get(field):
                    records[key]['native'] = dict(qualifiedName=binding[field], metaclass=kind)
    for machine in packet.get('stateMachines', []):
        for state in machine.get('states', []):
            key = machine['id'] + '/' + state['id']
            records[key] = dict(deepcopy(state), id=key, localId=state['id'], lifecycle=machine['id'],
                collection='states', category='Lifecycle state', sourceRefs=machine.get('sourceRefs', []),
                basis=machine.get('basis'), status=machine.get('status'))
        for transition in machine.get('transitions', []):
            key = machine['id'] + '/' + transition['id']
            records[key] = dict(deepcopy(transition), id=key, localId=transition['id'], lifecycle=machine['id'],
                source=machine['id'] + '/' + transition['from'], target=machine['id'] + '/' + transition['to'],
                label=transition.get('event') or transition.get('guard') or 'State transition',
                collection='stateTransitions', category='Lifecycle transition',
                sourceRefs=machine.get('sourceRefs', []), basis=machine.get('basis'), status=machine.get('status'))
    for key, record in records.items():
        binding = bindings.get('elements', {}).get(key)
        if binding:
            record['native'] = deepcopy(binding)
        elif record.get('lifecycle') in bindings.get('elements', {}):
            record['nativeContext'] = deepcopy(bindings['elements'][record['lifecycle']])
    return records


def hierarchy(packet, key):
    items = {x['id']: x for x in packet.get(key, [])}
    children = defaultdict(list)
    for item in items.values():
        if item.get('parent') and item['parent'] not in items:
            raise ValueError('Unknown hierarchy parent: ' + item['id'])
        children[item.get('parent')].append(item['id'])
    return items, children


def descendants(identity, children):
    found, pending = [], [identity]
    while pending:
        item = pending.pop(0)
        if item in found:
            raise ValueError('Cyclic architecture hierarchy')
        found.append(item)
        pending.extend(children.get(item, []))
    return found


def chunks(values, count=4):
    return [values[i:i + count] for i in range(0, len(values), count)]


def shortened(value, limit=74):
    text = ' '.join(str(value or '').split())
    return text if len(text) <= limit else text[:limit - 1].rsplit(' ', 1)[0] + '…'


class Graph:
    def __init__(self, records, section, mode, scope, label, question, note=''):
        self.records = records
        self.key = '|'.join((section, mode, scope))
        self.meta = dict(id=self.key, section=section, mode=mode, scope=scope, label=label,
                         question=question, note=note)
        self.nodes, self.edges, self.ranks = {}, [], []

    def node(self, identity, *, kind=None, boundary=False, suffix=''):
        if identity not in self.records:
            raise ValueError('Diagram node has no authored record: ' + identity)
        item = self.records[identity]
        self.nodes[identity] = dict(id=identity, label=item.get('label', identity),
                                   kind=kind or item.get('collection'), boundary=boundary, suffix=suffix)
        return identity

    def edge(self, identity, source, target, label='', *, kind='exchange', records=None, bidirectional=False):
        if source not in self.nodes or target not in self.nodes:
            raise ValueError('Diagram relationship has an unresolved visible endpoint')
        self.edges.append(dict(id=identity, source=source, target=target, label=label, kind=kind,
                               records=records or [identity], bidirectional=bidirectional))

    def synthetic(self, key, label, related, **extra):
        identity = 'projection:' + self.key + ':' + key
        self.records[identity] = dict(id=identity, label=label, category='Grouped presentation',
            collection='projectionGroups', status='derived display', basis='projection',
            relatedIds=related, sourceRefs=list(dict.fromkeys(s for i in related for s in self.records[i].get('sourceRefs', []))),
            description='A display grouping of explicit authored records. Inspect the members for exact model endpoints.', **extra)
        return identity

    def render(self, theme="paper"):
        from architecture_palette import paint, stylesheet
        names = {key: 'n' + str(i) for i, key in enumerate(self.nodes)}
        marks = {}
        q = lambda value: json.dumps(str(value), ensure_ascii=False)
        lines = ['digraph architecture {',
                 'graph [rankdir=TB, bgcolor="transparent", pad="0.32", nodesep="0.34", ranksep="0.52", splines=polyline, outputorder=edgesfirst, fontname="Arial"];',
                 'node [shape=box, style="rounded,filled", margin="0.16,0.12", fontname="Arial", fontsize=14, color="#527975", fillcolor="#eff7f4", fontcolor="#153c3a", penwidth=1.2];',
                 'edge [fontname="Arial", fontsize=10.5, color="#6b7e86", fontcolor="#40565e", arrowsize=0.7, penwidth=1.1];']
        lines = [stylesheet(line, theme) for line in lines]
        for identity, node in self.nodes.items():
            mark = 'mark-' + digest((self.key + ':node:' + identity).encode())[:16]
            marks[mark] = (identity, 'node')
            label = '\n'.join(textwrap.wrap(node['label'], width=29, break_long_words=False))
            if node['suffix']:
                label += '\n' + node['suffix']
            kind = node['kind']
            attrs = dict(id=mark, label=label, tooltip=node['label'])
            if kind in ('actors',):
                attrs.update(shape='box', fillcolor='#fff7e7', color='#b59959', fontcolor='#5c471c')
            elif kind in ('operationalActivities',):
                attrs.update(shape='ellipse', fillcolor='#e7f5ef', color='#4c8a73')
            elif kind in ('logicalComponents',):
                attrs.update(shape='box', fillcolor='#eaf0fb', color='#7586b0', fontcolor='#263d69')
            elif kind in ('states',):
                attrs.update(fillcolor='#edf0fb', color='#7b86b2', fontcolor='#34416c')
            elif kind == 'terminal':
                attrs.update(peripheries='2', fillcolor='#edf0fb', color='#7b86b2')
            elif kind in ('fork', 'join'):
                attrs.update(shape='rect', style='filled', fixedsize='true', width='1.8', height='0.12',
                             fillcolor='#335e59', color='#335e59', label='', xlabel=node['label'], fontsize='10')
            if node['boundary']:
                attrs.update(style='rounded,dashed,filled', fillcolor='#f6f6f3', color='#a8afa9', fontcolor='#596660')
            lines.append(names[identity] + ' [' + ','.join(k + '=' + q(paint(v,theme) if k in ('color','fillcolor','fontcolor') else v) for k, v in attrs.items()) + '];')
        for index, edge in enumerate(self.edges):
            mark = 'mark-' + digest((self.key + ':edge:' + str(index)).encode())[:16]
            marks[mark] = (edge['id'], 'edge')
            attrs = dict(id=mark, label='\n'.join(textwrap.wrap(shortened(edge['label']), 25, break_long_words=False)), tooltip=edge['label'])
            if edge['bidirectional']:
                attrs.update(dir='both', arrowtail='normal')
            if edge['kind'] in ('decomposition', 'participates'):
                attrs.update(color='#a0aaa4', fontcolor='#718078', arrowsize='0.5')
            elif edge['kind'] in ('allocation', 'realizes'):
                attrs.update(style='dashed', color='#7586b0', fontcolor='#4a5b83')
            elif edge['kind'] in ('guard', 'transition'):
                attrs.update(color='#588b86', fontcolor='#355f5a')
            if self.ranks:
                attrs['constraint'] = 'false'
            lines.append(names[edge['source']] + ' -> ' + names[edge['target']] + ' [' + ','.join(k + '=' + q(paint(v,theme) if k in ('color','fillcolor','fontcolor') else v) for k, v in attrs.items()) + '];')
        previous = None
        for i, rank in enumerate(self.ranks):
            rank = [x for x in rank if x in names]
            if not rank:
                continue
            lines.append('{rank=same; ' + ';'.join(names[x] for x in rank) + ';}')
            if previous:
                lines.append(names[previous] + ' -> ' + names[rank[0]] + ' [style=invis,weight=30];')
            previous = rank[-1]
        lines.append('}')
        run = subprocess.run(['dot', '-Tsvg'], input='\n'.join(lines), capture_output=True, text=True, check=True, timeout=30)
        root = ET.fromstring(run.stdout)
        root.set('role', 'img')
        root.set('aria-label', self.meta['question'])
        root.set('data-view-id', self.key)
        root.set('class', 'architecture-svg')
        for element in root.iter():
            mark = marks.get(element.get('id'))
            if mark:
                identity, kind = mark
                element.set('data-record-id', identity)
                element.set('data-mark-kind', kind)
                element.set('tabindex', '0')
                element.set('role', 'button')
                element.set('aria-label', 'Inspect ' + self.records.get(identity, {}).get('label', identity))
        raw = ET.tostring(root, encoding='unicode')
        filename = re.sub('[^a-z0-9_-]+', '-', self.key.lower()).strip('-') + '.svg'
        return dict(self.meta, svg=raw, file='diagrams/' + filename,
                    nodeCount=len(self.nodes), relationCount=len(self.edges),
                    nodes=list(self.nodes), relationIds=[e['id'] for e in self.edges])


def make_views(packet, records, theme="paper"):
    graphs = []
    functions, fc = hierarchy(packet, 'functions')
    components, cc = hierarchy(packet, 'logicalComponents')
    activities, ac = hierarchy(packet, 'operationalActivities')
    allocations = {a['function']: a for a in packet.get('allocations', [])}
    roots = fc.get(None, [])
    groups = [x for root in roots for x in fc.get(root, [])] or roots

    def group_of(identity):
        while identity in functions and functions[identity].get('parent') not in roots + [None]:
            identity = functions[identity]['parent']
        return identity

    for activity in activities.values():
        if not activity.get('parent'):
            continue
        selected = [activity['id']] + ac.get(activity['id'], [])
        g = Graph(records, 'operational', 'activities', activity['id'], activity['label'],
                  'Who performs and participates in this operational outcome?',
                  'Activities describe the participants’ work. These links express responsibility and participation, not a temporal sequence.')
        people = []
        for aid in selected:
            item = activities[aid]
            g.node(aid)
            for actor in [item.get('performer')] + item.get('participants', []):
                if not actor:
                    continue
                if actor not in people:
                    people.append(actor)
                g.node(actor)
                kind = 'performs' if actor == item.get('performer') else 'participates'
                link = g.synthetic(actor + '-' + aid, records[actor]['label'] + ' · ' + kind,
                                   [actor, aid], source=actor, target=aid, relation=kind)
                g.edge(link, actor, aid, kind, kind=kind)
        g.ranks = chunks(people) + chunks(selected, 3)
        graphs.append(g)
    for component in components.values():
        contacts = [x for x in packet.get('contextExchanges', []) if x['target'] == component['id'] or x['source'] == component['id']]
        if not contacts:
            continue
        g = Graph(records, 'operational', 'boundary', component['id'], component['label'],
                  'What crosses this candidate service boundary, and who retains authority?',
                  'Boundary contracts are proposed information and service exchanges. They do not transfer airline, agency or service-provider decision rights.')
        g.node(component['id'])
        actors = []
        for x in contacts:
            for endpoint in (x['source'], x['target']):
                g.node(endpoint)
                if endpoint != component['id'] and endpoint not in actors:
                    actors.append(endpoint)
            g.edge(x['id'], x['source'], x['target'], x.get('item', x['label']))
        g.ranks = chunks(actors) + [[component['id']]]
        graphs.append(g)
    for group in roots + groups:
        children = fc.get(group, [])
        if children:
            g = Graph(records, 'functions', 'decomposition', group, functions[group]['label'],
                      'Which smaller responsibilities compose this function?',
                      'Parent–child links express functional decomposition. They do not imply execution order or data transfer.')
            g.node(group)
            for child in children:
                g.node(child)
                link = g.synthetic('parent-' + child, 'Decomposes ' + functions[group]['label'],
                                   [group, child], source=group, target=child, relation='decomposition')
                g.edge(link, group, child, '', kind='decomposition')
            g.ranks = [[group]] + chunks(children)
            graphs.append(g)
        if group not in groups:
            continue
        local = set(descendants(group, fc))
        leafs = [x for x in local if not fc.get(x)]
        touching = [x for x in packet.get('exchanges', []) if x['source'] in local or x['target'] in local]
        g = Graph(records, 'functions', 'flow', group, functions[group]['label'],
                  'What does each function produce, consume and exchange across this slice?',
                  'Solid arrows are explicit functional exchanges. Dashed boundary nodes group outside functions; select an arrow to see the exact endpoints and applicability.')
        for leaf in sorted(leafs, key=lambda x: list(functions).index(x)):
            g.node(leaf)
        bundles = defaultdict(list)
        for x in touching:
            a = x['source'] if x['source'] in local else group_of(x['source'])
            b = x['target'] if x['target'] in local else group_of(x['target'])
            g.node(a, boundary=a not in local)
            g.node(b, boundary=b not in local)
            bundles[(a, b)].append(x)
        for (a, b), items in bundles.items():
            identities = [x['id'] for x in items]
            rid = identities[0] if len(items) == 1 else g.synthetic(a + '-' + b, str(len(items)) + ' explicit exchanges', identities, source=a, target=b)
            g.edge(rid, a, b, items[0].get('item', items[0]['label']) if len(items) == 1 else str(len(items)) + ' explicit exchanges', records=identities)
        graphs.append(g)
    for root in cc.get(None, []):
        children = cc.get(root, [])
        if children:
            g = Graph(records, 'logical', 'decomposition', root, components[root]['label'],
                      'How is the proposed logical service responsibility divided?',
                      'This is a logical responsibility decomposition. People, procedures and technology can realize it; equipment and products are not selected here.')
            g.node(root)
            for child in children:
                g.node(child)
                rid = g.synthetic('contains-' + child, 'Logical responsibility decomposition', [root, child], source=root, target=child)
                g.edge(rid, root, child, '', kind='decomposition')
            g.ranks = [[root]] + chunks(children, 3)
            graphs.append(g)
    for component in components.values():
        assigned = [a for a in packet.get('allocations', []) if a['component'] == component['id']]
        if not assigned:
            continue
        g = Graph(records, 'logical', 'allocation', component['id'], component['label'],
                  'Which functions are assigned to this logical responsibility?',
                  'Dashed arrows are explicit candidate allocations. A logical allocation does not approve an organisational owner or a technology solution.')
        g.node(component['id'])
        for allocation in assigned:
            g.node(allocation['function'])
            g.edge(allocation['id'], allocation['function'], component['id'], '', kind='allocation')
        g.ranks = chunks([a['function'] for a in assigned]) + [[component['id']]]
        graphs.append(g)
        interfaces = defaultdict(list)
        for x in packet.get('exchanges', []):
            a = allocations.get(x['source'], {}).get('component')
            b = allocations.get(x['target'], {}).get('component')
            if a and b and a != b and component['id'] in (a, b):
                neighbor = b if a == component['id'] else a
                interfaces[neighbor].append((x, a == component['id']))
        if interfaces:
            g = Graph(records, 'logical', 'interfaces', component['id'], component['label'],
                      'Which service contracts follow from the function allocations?',
                      'One contract groups each neighboring responsibility. Sent/received counts are relative to the selected scope; arrowheads preserve the declared directions. Inspect a contract for exact payloads and function endpoints.')
            g.node(component['id'])
            neighbors = []
            for neighbor, items in interfaces.items():
                g.node(neighbor); neighbors.append(neighbor)
                sent = sum(outgoing for _, outgoing in items)
                received = len(items) - sent
                a, b = (component['id'], neighbor) if sent else (neighbor, component['id'])
                title = str(sent) + ' sent · ' + str(received) + ' received'
                rid = g.synthetic(component['id'] + '-' + neighbor, title, [x['id'] for x, _ in items], source=a, target=b,
                                  derivation='Functional exchanges composed with candidate primary allocations; counts relative to ' + component['label'])
                g.edge(rid, a, b, title, bidirectional=bool(sent and received))
            g.ranks = chunks(neighbors[:len(neighbors) // 2], 3) + [[component['id']]] + chunks(neighbors[len(neighbors) // 2:], 3)
            graphs.append(g)
    for scenario in packet.get('scenarios', []):
        g = Graph(records, 'scenarios', 'scenario', scenario['id'], scenario['label'],
                  'How does this case progress, branch and recover under its declared conditions?',
                  'Arrows follow explicit guarded transitions. Guards are review predicates, not evaluated values; no simulation, guard exclusivity or successful outcome is asserted.')
        for step in scenario.get('steps', []):
            suffix = 'Entry step' if step['id'] == scenario.get('entryStep') else 'Conditional exit' if step['id'] in scenario.get('exitGuards', {}) else 'Declared exit' if step['id'] in scenario.get('exitSteps', []) else ''
            g.node(scenario['id'] + '/' + step['id'], suffix=suffix)
        branches, joins = {}, {}
        for group in scenario.get('parallelGroups', []):
            prefix = scenario['id'] + '/' + group['id']
            fork, join = prefix + '/fork', prefix + '/join'
            g.node(fork, kind='fork'); g.node(join, kind='join')
            g.edge(prefix + '/entryLink', scenario['id'] + '/' + group['from'], fork, '', kind='guard')
            g.edge(prefix + '/exitLink', join, scenario['id'] + '/' + group['join'], '', kind='guard')
            for transition in scenario.get('transitions', []):
                if transition['from'] == group['from'] and transition['to'] in group['branches'] and transition.get('kind') == 'parallel':
                    branches[transition['id']] = fork
                if transition['to'] == group['join'] and transition.get('kind') == 'join':
                    joins[transition['id']] = join
        for transition in scenario.get('transitions', []):
            a = branches.get(transition['id'], scenario['id'] + '/' + transition['from'])
            b = joins.get(transition['id'], scenario['id'] + '/' + transition['to'])
            if transition['id'] in branches or transition['id'] in joins:
                records[transition['id']]['displaySource'] = a
                records[transition['id']]['displayTarget'] = b
            g.edge(transition['id'], a, b,
                   transition.get('condition') or transition.get('outcome', ''), kind='guard')
        graphs.append(g)
    for machine in packet.get('stateMachines', []):
        g = Graph(records, 'scenarios', 'states', machine['id'], machine['label'],
                  'Which events and guards change the service state, and what obligation follows?',
                  'States and transitions are proposed lifecycle logic. Entry, terminal and continuing-operation conditions remain explicit; no state is presented as observed.')
        for state in machine.get('states', []):
            terminal = state['id'] in machine.get('terminalStates', [])
            suffix = 'Initial state' if state['id'] == machine.get('initial') else 'Declared terminal' if terminal else ''
            g.node(machine['id'] + '/' + state['id'], kind='terminal' if terminal else 'states', suffix=suffix)
        for transition in machine.get('transitions', []):
            rid = machine['id'] + '/' + transition['id']
            g.edge(rid, machine['id'] + '/' + transition['from'], machine['id'] + '/' + transition['to'],
                   transition.get('event') or transition.get('guard', ''), kind='transition')
        graphs.append(g)
    return {g.key: g.render(theme) for g in graphs}


def assurance(checks, architecture_raw, model_raw, bindings_raw):
    match = bool(checks and checks.get('architectureSha256') == digest(architecture_raw)
                 and checks.get('modelSha256') == digest(model_raw)
                 and checks.get('bindingsSha256') == digest(bindings_raw))
    native = bool(match and checks.get('nativeValidation') == 'managed-report-and-facts-checked'
                  and checks.get('native', {}).get('passed') is True
                  and checks.get('structuralConsistencyPassed') is True)
    annotations = checks.get('native', {}).get('annotationsOnly', []) if checks else []
    scope = checks.get('native', {}).get('nativeProjectionScope', []) if checks else []
    annotation_note = (' ' + ', '.join(COLLECTIONS.get(name, name).lower() for name in annotations).capitalize()
                       + ' remain authored review annotations.') if annotations else ''
    return dict(nativeChecked=native, receiptMatches=match,
                label='Native structure checked · engineering review open' if native else 'Authored architecture projection · native confirmation pending',
                explanation=('Resolved native identities and relationships were checked against this exact model and recipe.' + annotation_note + ' Engineering decisions and planned verification remain open.' if native else
                             'Diagrams follow the explicit authored recipe and matching model bindings. No matching successful native-check receipt is supplied.'),
                nativeProjectionScope=scope, annotationsOnly=annotations,
                structuralConsistency=checks.get('structuralConsistencyPassed') if checks else None,
                reviewReadiness=checks.get('reviewReadiness', 'not assessed') if checks else 'not assessed')


def build(architecture, model, bindings, output, *, checks=None, evidence=None, theme="paper"):
    architecture, model, bindings, output = map(Path, (architecture, model, bindings, output))
    raw, model_raw, bindings_raw = architecture.read_bytes(), model.read_bytes(), bindings.read_bytes()
    packet, mapping = json.loads(raw), json.loads(bindings_raw)
    if mapping.get('modelSha256') != digest(model_raw):
        raise ValueError('Bindings do not match these exact model bytes')
    if mapping.get('recipeSha256') != recipe_digest(packet):
        raise ValueError('Bindings do not match this architecture recipe')
    if any((output / p).exists() for p in ('review.html', 'diagrams', 'reader-data.json')):
        raise ValueError('Reader-owned files already exist; use a new export directory')
    check_raw = Path(checks).read_bytes() if checks else None
    check_data = json.loads(check_raw) if check_raw else None
    legacy = json.loads(Path(evidence).read_bytes()) if evidence else {}
    records = record_index(packet, mapping)
    views = make_views(packet, records, theme)
    legacy_records = []
    for item in legacy.get('records', []):
        legacy_records.append({k: deepcopy(item[k]) for k in ('id', 'label', 'kind', 'text', 'section', 'chapter', 'pages', 'status', 'q') if k in item})
    payload = dict(schemaVersion=1, role='question-led-architecture-reader', architecture=packet,
                   records=records, views=views, assurance=assurance(check_data, raw, model_raw, bindings_raw),
                   checks=check_data, evidence=legacy_records,
                   modelSha256=digest(model_raw), recipeSha256=recipe_digest(packet), sourcePdf=None,
                   downloads=dict(model='model.sysml', architecture='architecture.json', bindings='bindings.json'))
    files = {'model.sysml': model_raw, 'architecture.json': raw, 'bindings.json': bindings_raw}
    if check_raw:
        files['architecture-checks.json'] = check_raw
        payload['downloads']['checks'] = 'architecture-checks.json'
    source_pdf = Path(evidence).parent / packet.get('source', {}).get('file', 'source.pdf') if evidence else None
    if source_pdf and source_pdf.is_file() and source_pdf.suffix.lower() == '.pdf':
        pdf_raw = source_pdf.read_bytes()
        if packet.get('source', {}).get('sha256') == digest(pdf_raw):
            files['sources/source.pdf'] = pdf_raw
            payload['sourcePdf'] = 'sources/source.pdf'
    # All expensive work and collision checks precede publication. Existing
    # emitter-owned model files are reused only if their bytes are identical.
    for name, content in files.items():
        target = output / name
        if target.exists() and target.read_bytes() != content:
            raise ValueError('Export would replace a different input artifact: ' + name)
    from architecture_palette import stylesheet
    template = (HERE / 'architecture_review.html').read_text()
    page = template.replace('<!-- READER_CSS -->', '<style>' + stylesheet((HERE / 'architecture_review.css').read_text(), theme) + '</style>')
    page = page.replace('<!-- READER_DATA -->', '<script type="application/json" id="reader-data">' + encoded(payload) + '</script>')
    page = page.replace('<!-- READER_JS -->', '<script>' + (HERE / 'architecture_review.js').read_text() + '</script>')
    page = page.replace('<!-- PAGE_TITLE -->', html.escape(packet.get('title', 'Architecture review')))
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = output / name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(content)
    (output / 'diagrams').mkdir()
    for view in views.values():
        (output / view['file']).write_text(view['svg'], encoding='utf-8')
    with (output / 'review.html').open('x', encoding='utf-8') as stream:
        stream.write(page)
    return dict(entry=str(output / 'review.html'), diagrams=len(views), records=len(records),
                evidenceRecords=len(legacy_records), nativeChecked=payload['assurance']['nativeChecked'],
                modelSha256=payload['modelSha256'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('architecture', 'model', 'bindings', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    parser.add_argument('--theme', choices=['paper','blueprint','ink'], default='paper')
    parser.add_argument('--checks', type=Path)
    parser.add_argument('--evidence', type=Path, help='Optional legacy whole-data.json source inventory')
    args = parser.parse_args()
    print(json.dumps(build(args.architecture, args.model, args.bindings, args.output,
                           checks=args.checks, evidence=args.evidence, theme=args.theme), indent=2))


if __name__ == '__main__':
    main()
