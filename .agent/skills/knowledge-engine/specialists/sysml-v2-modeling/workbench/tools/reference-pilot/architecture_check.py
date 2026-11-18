#!/usr/bin/env python3
"""Check an authored architecture recipe, then optionally its resolved native bindings.

This is an engineering review aid, not a source-entailment or design-approval
oracle. Topology checks use explicit IDs and typed relations, never label words.
Native checks consume a managed language-engine report; JSON-only checks never
claim that SysML has been parsed, resolved, simulated or accepted.
"""
import argparse
from collections import defaultdict, deque
import hashlib
import json
from pathlib import Path


COLLECTIONS = (
    'actors', 'operationalActivities', 'functions', 'exchanges',
    'logicalComponents', 'allocations', 'scenarios', 'requirements',
    'verificationCases', 'decisions', 'stateMachines', 'insights',
    'contextExchanges', 'parameters',
)
NATIVE_KINDS = {
    'actors': {'PartUsage'}, 'operationalActivities': {'ActionUsage'},
    'functions': {'ActionUsage'}, 'exchanges': {'FlowUsage', 'SuccessionFlowUsage'},
    'logicalComponents': {'PartUsage'}, 'allocations': {'AllocationUsage'},
    'scenarios': {'ActionUsage'}, 'requirements': {'RequirementUsage'},
    'verificationCases': {'VerificationCaseDefinition', 'VerificationCaseUsage'},
    'stateMachines': {'StateDefinition', 'StateUsage', 'ExhibitStateUsage'},
    'contextExchanges': {'InterfaceUsage'},
}
BASES = {'source-explicit', 'derived', 'proposed'}
OPEN = {'open', 'unresolved', 'partial', 'pending'}
CLAIMED_ACCEPTED = {'accepted', 'approved', 'verified', 'passed', 'satisfied'}
SI_DURATION_NAMES = {'s': 'SI::second', 'min': 'SI::minute', 'h': 'SI::hour', 'd': 'SI::day'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def reached(start, adjacency):
    seen, queue = set(), deque(start)
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(adjacency.get(node, ()))
    return seen


def formal_constraint_matches(expression, formal, subject_name, attribute_name):
    """Compare bounded native syntax facts, including units; do not evaluate it."""
    operands = expression.get('operands', [])
    if (expression.get('kind') != 'OperatorExpression' or expression.get('operator') != formal.get('operator')
            or len(operands) != 2 or not attribute_name
            or operands[0] != {'kind': 'FeaturePath', 'path': [subject_name, attribute_name]}):
        return False
    right = operands[1]
    if formal.get('quantity') == 'duration':
        unit = SI_DURATION_NAMES.get(formal.get('unit'))
        terms = right.get('operands', [])
        if (not unit or right.get('kind') != 'OperatorExpression' or right.get('operator') != '[' or len(terms) != 2
                or terms[1] != {'kind': 'FeaturePath', 'path': [unit]}):
            return False
        right = terms[0]
    elif formal.get('quantity') != 'number':
        return False
    sign = 1
    if right.get('kind') == 'OperatorExpression' and right.get('operator') == '-' and len(right.get('operands', [])) == 1:
        sign, right = -1, right['operands'][0]
    return (right.get('kind') in {'LiteralInteger', 'LiteralRational', 'LiteralReal'}
            and type(right.get('value')) in (int, float) and sign * right['value'] == formal.get('value'))


def check_architecture(packet):
    """Return separate consistency and completeness findings for one recipe."""
    issues = []

    def issue(code, subject, message, severity='error'):
        issues.append(dict(code=code, subject=subject, severity=severity, message=message))

    if not isinstance(packet, dict):
        return {'schemaVersion': 1, 'structuralConsistencyPassed': False,
                'reviewReadiness': 'invalid', 'issues': [dict(code='packet-shape',
                subject='architecture', severity='error', message='Architecture must be an object.')],
                'nativeValidation': 'not-assessed', 'engineeringAcceptance': 'not-assessed'}
    if type(packet.get('schemaVersion', 1)) not in (int, str) or packet.get('schemaVersion', 1) not in (1, '1.0.0'):
        issue('schema-version', 'architecture', 'Unsupported architecture schemaVersion.')
    scope = packet.get('scope', {})
    if not isinstance(scope, dict):
        scope = {}
    for key in ('name', 'boundary', 'phase', 'decision'):
        if not nonempty(scope.get(key)):
            issue('missing-scope', 'scope.' + key, 'State the ' + key + ' used to tailor this study.')
    for key in ('included', 'excluded'):
        if not isinstance(scope.get(key), list) or any(not nonempty(v) for v in scope[key]):
            issue('scope-list', 'scope.' + key, 'Use a list of explicit scope statements; an empty exclusion list is allowed.')

    groups, index, kinds = {}, {}, {}
    for kind in COLLECTIONS:
        records = packet.get(kind, [])
        if not isinstance(records, list):
            issue('collection-shape', kind, 'Expected a list.'); records = []
        groups[kind] = []
        for position, record in enumerate(records):
            loc = kind + '[' + str(position) + ']'
            if not isinstance(record, dict) or not nonempty(record.get('id')):
                issue('record-identity', loc, 'Every record needs an explicit stable id.'); continue
            key = record['id']
            if key in index:
                issue('duplicate-id', key, 'IDs must be unique across architecture collections.'); continue
            index[key], kinds[key] = record, kind
            groups[kind].append(record)
            if kind not in ('allocations', 'decisions', 'insights') and not nonempty(record.get('label')):
                issue('record-label', key, 'Provide a reader-facing label, separate from the id.')
            if record.get('basis') not in BASES:
                issue('assertion-basis', key, 'Use source-explicit, derived or proposed basis.')
            refs = record.get('sourceRefs', [])
            if not isinstance(refs, list) or any(not nonempty(r) for r in refs):
                issue('source-reference-shape', key, 'Source references must be nonempty locator strings.')
            elif record.get('basis') == 'source-explicit' and not refs:
                issue('uncited-source-claim', key, 'A source-explicit claim needs a source locator.')
            if not nonempty(record.get('status')):
                issue('missing-status', key, 'Retain assertion or decision status.')
            elif record['status'].lower() in CLAIMED_ACCEPTED and not record.get('acceptanceEvidence'):
                issue('unsupported-acceptance', key, 'A modeled assertion is not accepted/verified without identified acceptance evidence.')
            if isinstance(record.get('status'), str) and record['status'].lower() in OPEN:
                issue('open-assertion', key, 'This assertion remains ' + record['status'] + '.', 'review')

    def ref(value, allowed, owner, field, optional=False):
        if optional and value in (None, ''):
            return False
        if not isinstance(value, str) or value not in index:
            issue('unresolved-reference', owner, field + ' must resolve to a declared ' + '/'.join(allowed) + ' id.')
            return False
        if kinds[value] not in allowed:
            issue('wrong-reference-kind', owner, field + ' points to ' + kinds[value] + ', not ' + '/'.join(allowed) + '.')
            return False
        return True

    def refs(values, allowed, owner, field, required=False):
        if not isinstance(values, list):
            issue('reference-list', owner, field + ' must be a list of IDs.'); return []
        if required and not values:
            issue('missing-related-evidence', owner, field + ' is empty.', 'review')
        return [v for v in values if ref(v, allowed, owner, field)]

    # Parent links are same-level decomposition, not untyped trace edges.
    children = defaultdict(set)
    for kind in ('operationalActivities', 'functions', 'logicalComponents'):
        for record in groups[kind]:
            if record.get('parent'):
                if ref(record['parent'], {kind}, record['id'], 'parent'):
                    children[record['parent']].add(record['id'])
        for record in groups[kind]:
            seen, current = set(), record
            while current.get('parent') in index:
                if current['id'] in seen:
                    issue('cyclic-decomposition', record['id'], 'Decomposition must not contain a parent cycle.'); break
                seen.add(current['id']); current = index[current['parent']]

    for activity in groups['operationalActivities']:
        if not activity.get('performer'):
            issue('missing-performer', activity['id'], 'Operational activity has no identified performer.', 'review')
        else:
            ref(activity['performer'], {'actors'}, activity['id'], 'performer')
    leaves = [f for f in groups['functions'] if not children[f['id']]]
    for function in groups['functions']:
        refs(function.get('realizes', []), {'operationalActivities'}, function['id'], 'realizes', required=function in leaves)
        if function.get('level', 'system') != 'system':
            issue('function-level', function['id'], 'This schema distinguishes system functions from operational activities and logical components.')

    adjacency, exchange_signatures = defaultdict(set), {}
    for exchange in groups['exchanges']:
        key = exchange['id']
        good_source = ref(exchange.get('source'), {'functions'}, key, 'source')
        good_target = ref(exchange.get('target'), {'functions'}, key, 'target')
        for field in ('item', 'condition'):
            if not nonempty(exchange.get(field)):
                issue('incomplete-exchange', key, 'An exchange needs explicit ' + field + '.', 'review')
        if exchange.get('kind') not in ('object', 'control', 'data'):
            issue('exchange-kind', key, 'Distinguish object, control and data exchanges.')
        if good_source and good_target:
            a, b = exchange['source'], exchange['target']
            adjacency[a].add(b); adjacency[b].add(a)
            signature = (a, b, json.dumps([exchange.get('kind'), exchange.get('item'), exchange.get('condition')], sort_keys=True))
            if signature in exchange_signatures and not exchange.get('distinctReason'):
                issue('duplicate-exchange', key, 'Same exchange as ' + exchange_signatures[signature] + '; reuse it or state the distinct occurrence.', 'review')
            exchange_signatures[signature] = key
    for function in leaves:
        if not adjacency[function['id']] and not nonempty(function.get('isolationReason')):
            issue('disconnected-function', function['id'], 'Leaf function has no explicit functional exchange; model its interaction or state the scoped reason.', 'review')

    assigned = defaultdict(list)
    for allocation in groups['allocations']:
        key = allocation['id']
        f_ok = ref(allocation.get('function'), {'functions'}, key, 'function')
        c_ok = ref(allocation.get('component'), {'logicalComponents'}, key, 'component')
        if not nonempty(allocation.get('rationale')):
            issue('allocation-rationale', key, 'Allocation needs a design responsibility rationale.', 'review')
        if f_ok and c_ok:
            assigned[allocation['function']].append(allocation['component'])
    logical_required = bool(groups['logicalComponents']) or 'logical' in str(scope.get('phase', '')).lower()
    if logical_required:
        for function in leaves:
            if not assigned[function['id']]:
                issue('unallocated-function', function['id'], 'No logical responsibility is allocated to this in-scope leaf function.', 'review')
        for function, components in assigned.items():
            if len(components) > 1 and not nonempty(index[function].get('allocationRationale')):
                issue('multiple-allocation', function, 'Explain collaboration or alternatives between multiple allocated components.', 'review')

    def scenario_graph(record, steps, transitions, node_field):
        key = record['id']
        if not isinstance(steps, list) or not isinstance(transitions, list):
            issue('scenario-shape', key, 'Steps/states and transitions must be lists.'); return
        nodes, forward, backward, edge_ids = {}, defaultdict(set), defaultdict(set), set()
        for step in steps:
            if not isinstance(step, dict) or not nonempty(step.get('id')):
                issue('step-identity', key, 'Every step/state needs an id.'); continue
            if step['id'] in nodes or step['id'] in ('start', 'done'):
                issue('duplicate-step', key, 'Step IDs must be unique and cannot shadow start/done.'); continue
            nodes[step['id']] = step
            if node_field:
                ref(step.get(node_field), {'functions'}, key + '/' + step['id'], node_field)
                if step.get('actor'):
                    ref(step['actor'], {'actors'}, key + '/' + step['id'], 'actor')
        if not nodes:
            issue('empty-scenario', key, 'A scenario/state machine needs explicit steps/states.'); return
        start = record.get('entryStep', record.get('initial', next(iter(nodes))))
        endings = record.get('exitSteps', record.get('terminalStates', record.get('final')))
        if isinstance(endings, str): endings = [endings]
        allowed = set(nodes) | {'start', 'done'}
        if not isinstance(start, str) or start not in allowed:
            issue('scenario-boundary', key, 'Initial/final nodes must resolve within this scenario.')
            start = next(iter(nodes))
        conditions = defaultdict(list)
        parallel_origins = set()
        for edge in transitions:
            if not isinstance(edge, dict) or not nonempty(edge.get('id')):
                issue('transition-identity', key, 'Every transition needs an id.'); continue
            if edge['id'] in edge_ids: issue('duplicate-transition', key, 'Transition IDs must be unique.')
            edge_ids.add(edge['id'])
            a, b = edge.get('from'), edge.get('to')
            if not isinstance(a, str) or not isinstance(b, str) or a not in allowed or b not in allowed:
                issue('dangling-transition', key + '/' + edge['id'], 'Transition endpoints must be declared steps/states or start/done.'); continue
            forward[a].add(b); backward[b].add(a)
            condition = edge.get('condition', edge.get('guard', ''))
            conditions[a].append(condition if isinstance(condition, str) else '')
            if not nonempty(condition):
                issue('unspecified-transition-condition', key + '/' + edge['id'], 'Declare the condition, including unconditional completion where applicable.', 'review')
            if not node_field and a != 'start' and not nonempty(edge.get('event')):
                issue('missing-state-event', key + '/' + edge['id'], 'State transition needs its triggering event.', 'review')
        if node_field:
            declared_controls = set()
            groups = record.get('parallelGroups', [])
            if not isinstance(groups, list):
                issue('parallel-group-shape', key, 'parallelGroups must be a list.'); groups = []
            for group in groups:
                gid = key + '/' + str(group.get('id', '?')) if isinstance(group, dict) else key
                if not isinstance(group, dict) or not nonempty(group.get('id')):
                    issue('parallel-group-shape', gid, 'Concurrent obligations need an explicit group ID.'); continue
                origin, join, branches = group.get('from'), group.get('join'), group.get('branches')
                if (not isinstance(origin, str) or origin not in nodes or not isinstance(join, str) or join not in nodes
                        or not isinstance(branches, list) or len(branches) < 2
                        or any(not isinstance(b, str) or b not in nodes for b in branches)
                        or len(set(branches)) != len(branches)):
                    issue('parallel-group-endpoints', gid, 'A parallel group needs a declared source, at least two distinct branch steps and a joining step.'); continue
                parallel_origins.add(origin)
                branches_out = [t for t in transitions if isinstance(t, dict) and t.get('from') == origin and t.get('to') in branches and t.get('kind') == 'parallel']
                joins_in = [t for t in transitions if isinstance(t, dict) and t.get('to') == join and t.get('kind') == 'join']
                if len(branches_out) != len(branches) or {t['to'] for t in branches_out} != set(branches) or len({t['from'] for t in joins_in}) < 2:
                    issue('parallel-group-links', gid, 'Each concurrent branch needs its fork link and a distinct completion contribution to the join.')
                for t in branches_out + joins_in:
                    if t['id'] in declared_controls:
                        issue('overlapping-parallel-group', gid, 'One transition cannot belong to two parallel groups.')
                    declared_controls.add(t['id'])
                bounded = {n: targets - {join} for n, targets in forward.items() if n != join}
                join_sources = {t['from'] for t in joins_in}
                for branch in branches:
                    branch_nodes = reached([branch], bounded)
                    contributions = [t for t in joins_in if t['from'] in branch_nodes]
                    if not contributions:
                        issue('parallel-obligation-missing', gid + '/' + branch, 'This branch has no completion path to the declared join.')
                    elif len(contributions) != 1:
                        issue('parallel-join-shape', gid + '/' + branch, 'This bounded profile requires one joining contribution per concurrent branch; branch alternatives need their own explicit merge.')
                    if any(n not in join_sources and not forward[n] for n in branch_nodes):
                        issue('parallel-join-bypass', gid + '/' + branch, 'A concurrent obligation can end without contributing to the join.')
            for t in transitions:
                if isinstance(t, dict) and t.get('kind') in ('parallel', 'join') and t.get('id') not in declared_controls:
                    issue('undeclared-parallel-link', key + '/' + str(t.get('id')), 'Concurrent/join links need an explicit parallel group.')
        if endings is None:
            endings = [n for n in nodes if not forward[n]]
        if not isinstance(endings, list) or any(not isinstance(n, str) or n not in allowed for n in endings):
            issue('scenario-exit', key, 'Final outcomes must be IDs in this scenario.'); endings = []
        ongoing = record.get('terminalPolicy') == 'ongoing'
        if not endings and not (ongoing and nonempty(record.get('lifecycleExitCondition'))):
            issue('scenario-exit', key, 'Declare terminal outcomes, or an ongoing lifecycle with its exit/review condition.', 'review')
        if start == 'start' and not forward['start']:
            issue('missing-start-transition', key, 'The scenario has no declared start path.', 'review')
        live = reached([start], forward)
        can_exit = reached(endings, backward)
        for node in nodes:
            if node not in live: issue('unreachable-step', key + '/' + node, 'This step/state is unreachable from the declared entry.')
            if node not in can_exit and not ongoing:
                issue('no-exit-path', key + '/' + node, 'No declared path reaches a final outcome from this step/state.', 'review')
        for node, values in conditions.items():
            if node not in parallel_origins and len(forward[node]) > 1 and (len(set(values)) != len(values) or any(not nonempty(v) for v in values)):
                issue('ambiguous-branch', key + '/' + node, 'Branches need distinguishable conditions; no exclusivity/exhaustiveness is inferred from prose.', 'review')

    for scenario in groups['scenarios']:
        for field in ('entryConditions', 'exitConditions'):
            v = scenario.get(field)
            if not (nonempty(v) or isinstance(v, list) and v and all(nonempty(x) for x in v)):
                issue('scenario-condition', scenario['id'], 'State ' + field + '.', 'review')
        scenario_graph(scenario, scenario.get('steps'), scenario.get('transitions'), 'function')
    for state in groups['stateMachines']:
        ref(state.get('subject'), {'functions', 'logicalComponents'}, state['id'], 'subject')
        scenario_graph(state, state.get('states'), state.get('transitions'), None)
    requested_kinds = scope.get('requiredScenarioKinds', [])
    if not isinstance(requested_kinds, list):
        issue('scenario-kind-contract', 'scope', 'requiredScenarioKinds must be a list.'); requested_kinds = []
    present_kinds = {s.get('kind') for s in groups['scenarios']}
    for kind in requested_kinds:
        if kind not in present_kinds:
            issue('missing-scenario-kind', 'scope', 'The requested ' + str(kind) + ' scenario has not been developed.', 'review')

    for requirement in groups['requirements']:
        key = requirement['id']
        ref(requirement.get('subject'), {'functions', 'logicalComponents'}, key, 'subject')
        for field in ('condition', 'criterion'):
            if not nonempty(requirement.get(field)) or requirement.get(field, '').strip().lower() in ('tbd', 'unknown', 'to be confirmed'):
                issue('undefined-requirement-' + field, key, 'An observable ' + field + ' remains unresolved.', 'review')
        if requirement.get('basis') in ('derived', 'proposed') and not nonempty(requirement.get('rationale')):
            issue('requirement-rationale', key, 'Derived/proposed requirements need their rationale.', 'review')
        refs(requirement.get('derivedFrom', []), set(COLLECTIONS), key, 'derivedFrom')
        refs(requirement.get('decisionIds', []), {'decisions'}, key, 'decisionIds')
        refs(requirement.get('parameterIds', []), {'parameters'}, key, 'parameterIds')
        if requirement.get('formalConstraint'):
            formal = requirement['formalConstraint']
            if (not isinstance(formal, dict) or not nonempty(formal.get('attribute'))
                    or formal.get('quantity') not in ('duration', 'number')
                    or formal.get('operator') not in ('>=', '<=', '==', '>', '<')
                    or type(formal.get('value')) not in (int, float)
                    or formal.get('quantity') == 'duration' and formal.get('unit') not in SI_DURATION_NAMES):
                issue('formal-constraint-shape', key, 'Formal criterion needs a supported subject attribute, comparator, numeric bound and explicit duration unit.')
        cases = refs(requirement.get('verificationIds', []), {'verificationCases'}, key, 'verificationIds', required=True)
        for case in cases:
            if key not in index[case].get('requirementIds', []):
                issue('verification-link-mismatch', key, 'Verification link is not reciprocal in ' + case + '.')
    for case in groups['verificationCases']:
        key = case['id']
        requirements = refs(case.get('requirementIds', []), {'requirements'}, key, 'requirementIds', required=True)
        if case.get('status') != 'planned':
            issue('verification-not-planned', key, 'This architecture recipe contains planned verification, not execution results.')
        for field in ('method', 'setup', 'expectedResult'):
            if not nonempty(case.get(field)):
                issue('incomplete-verification-plan', key, 'Verification plan lacks ' + field + '.', 'review')
        if any(field in case for field in ('actualResult', 'passed', 'executionDate')):
            issue('verification-result-in-plan', key, 'Keep executed results in a separate configuration-bound evidence record.')
        for requirement in requirements:
            if key not in index[requirement].get('verificationIds', []):
                issue('verification-link-mismatch', key, 'Requirement does not reference this plan: ' + requirement + '.')
    for decision in groups['decisions']:
        refs(decision.get('affects', []), set(COLLECTIONS) - {'decisions', 'insights'}, decision['id'], 'affects', required=True)
        if not nonempty(decision.get('question')):
            issue('decision-question', decision['id'], 'Retain the decision question.')
        if decision.get('status') == 'resolved' and not nonempty(decision.get('resolution')):
            issue('unsupported-resolution', decision['id'], 'A resolved decision needs a recorded disposition.')
        elif decision.get('status') not in ('resolved', 'closed', 'accepted', 'approved'):
            issue('unresolved-decision', decision['id'], 'The design decision has no recorded accepted disposition.', 'review')
    for insight in groups['insights']:
        refs(insight.get('relatedIds', []), set(COLLECTIONS) - {'insights'}, insight['id'], 'relatedIds')
    for exchange in groups['contextExchanges']:
        for end in ('source', 'target'):
            ref(exchange.get(end), {'actors', 'logicalComponents'}, exchange['id'], end)
        if not nonempty(exchange.get('item')):
            issue('context-exchange-item', exchange['id'], 'Identify the exchanged information, material or control obligation.', 'review')
        if exchange.get('kind') not in ('object', 'control', 'data'):
            issue('exchange-kind', exchange['id'], 'Distinguish object, control and data exchanges.')
    for parameter in groups['parameters']:
        if parameter.get('decisionId'):
            ref(parameter['decisionId'], {'decisions'}, parameter['id'], 'decisionId')
        if parameter.get('value') is None:
            issue('unresolved-parameter', parameter['id'], 'A criterion parameter has no agreed value.', 'review')

    concerns = {'operational': 'operationalActivities', 'system': 'functions',
                'logical': 'logicalComponents', 'requirements': 'requirements',
                'verification': 'verificationCases', 'states': 'stateMachines'}
    required = scope.get('requiredConcerns', [])
    if not isinstance(required, list):
        issue('concern-contract', 'scope', 'requiredConcerns must be a list.'); required = []
    for concern in required:
        if concern not in concerns:
            issue('unsupported-concern', 'scope', 'Unknown required concern: ' + str(concern))
        elif not groups[concerns[concern]]:
            issue('missing-concern', concern, 'The requested architecture concern has no developed records.', 'review')
    if not groups['functions'] or not groups['exchanges']:
        issue('architecture-empty', 'architecture', 'A catalogue of definitions/traces is not a connected system-function architecture.')

    coverage = packet.get('coverage', [])
    if isinstance(coverage, dict):
        if any(k in coverage for k in ('sourceSections', 'oldJourneyIds', 'slices')):
            entries = []
            for category, values in coverage.items():
                if not isinstance(values, list):
                    issue('coverage-shape', 'coverage.' + category, 'Use a list of trace dispositions.'); continue
                for value in values:
                    if not isinstance(value, dict):
                        issue('coverage-shape', 'coverage.' + category, 'Each disposition must be an object.'); continue
                    entry = dict(value)
                    entry['source'] = value.get('sourceSection', value.get('oldJourneyId', value.get('id', category)))
                    if category == 'slices':
                        entry['modelIds'] = value.get('scenarioIds', []) + ([value['functionRoot']] if value.get('functionRoot') else [])
                    entries.append(entry)
            coverage = entries
        else:
            coverage = [dict(value, source=key) if isinstance(value, dict) else dict(source=key, modelIds=value)
                        for key, value in coverage.items()]
    if not isinstance(coverage, list):
        issue('coverage-shape', 'coverage', 'Coverage must contain source-to-model mappings.'); coverage = []
    for position, row in enumerate(coverage):
        if not isinstance(row, dict):
            issue('coverage-shape', str(position), 'Coverage entry must be an object.'); continue
        values = row.get('modelIds', row.get('modelIDs', row.get('model_ids', [])))
        if values:
            refs(values, set(COLLECTIONS), 'coverage:' + str(position), 'modelIds')
        elif not nonempty(row.get('explanation', row.get('reason'))):
            issue('undisposed-source-scope', 'coverage:' + str(position), 'Map this source scope to model IDs or explain the unresolved/excluded portion.', 'review')
    errors = [i for i in issues if i['severity'] == 'error']
    review = [i for i in issues if i['severity'] == 'review']
    return {'schemaVersion': 1, 'profile': 'authored-architecture-review-v1',
            'structuralConsistencyPassed': not errors,
            'reviewReadiness': 'invalid' if errors else 'review-required' if review else 'candidate-ready-for-engineering-review',
            'counts': {k: len(v) for k, v in groups.items()}, 'issues': issues,
            'errorCount': len(errors), 'reviewItemCount': len(review),
            'nativeValidation': 'not-assessed', 'engineeringAcceptance': 'not-assessed',
            'limits': ['Explicit graph, responsibility, scenario and plan checks; source entailment and design adequacy require engineering review.',
                       'A qualitative criterion or guard remains qualitative; no predicate evaluation, simulation or operational acceptance is inferred.']}


def check_native_bindings(packet, report, bindings):
    """Compare authored identities/relationships with resolved native facts."""
    from check_contract import (check_contract, reference_path, references,
                                expression_fact, constraint_membership_kind,
                                documentation_facts)
    from engineering import index_report
    issues, relations, by_id = [], [], index_report(report)
    by_name = defaultdict(list)
    by_owner = defaultdict(list)
    for element in report.get('elements', []):
        if element.get('qualifiedName'):
            by_name[element['qualifiedName']].append(element)
        by_owner[element.get('semantics', {}).get('owner', {}).get('qualifiedName')].append(element)

    def issue(code, subject, message):
        issues.append(dict(code=code, subject=subject, severity='error', message=message))

    mapped = bindings.get('elements', {}) if isinstance(bindings, dict) else {}
    if not isinstance(mapped, dict):
        return {'passed': False, 'issues': [dict(code='native-bindings-shape', subject='bindings', severity='error', message='elements must be an ID mapping.')]}
    if report.get('staticChecksPassed') is not True:
        issue('native-language-failed', 'model', 'The language engine did not accept this model.')
    if bindings.get('modelSha256') != report.get('sourceSha256'):
        issue('native-source-mismatch', 'model', 'Bindings and native report refer to different model bytes.')
    recipe_sha = hashlib.sha256(json.dumps(packet, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    if bindings.get('recipeSha256') != recipe_sha:
        issue('native-recipe-mismatch', 'architecture', 'Bindings were not generated from this exact authored recipe.')
    resolved = {}

    def locate(key, allowed, qname=None):
        binding = mapped.get(key, {})
        if qname is None:
            qname = binding if isinstance(binding, str) else binding.get('qualifiedName')
        candidates = by_name.get(qname, [])
        if len(candidates) != 1:
            issue('native-identity-missing', key, 'Expected one resolved native element for this authored identity.')
            return None
        element = candidates[0]
        if element.get('metaclass') not in allowed:
            issue('native-kind-mismatch', key, 'Expected ' + '/'.join(sorted(allowed)) + ', found ' + str(element.get('metaclass')) + '.')
            return None
        return element

    for group, allowed in NATIVE_KINDS.items():
        for record in packet.get(group, []):
            key = record['id']
            element = locate(key, allowed)
            if element is None: continue
            resolved[key] = element
            # This adapter preserves epistemic metadata as explicit documentation.
            # Checking retention is not an assessment that a source entails it.
            docs = '\n'.join(d['body'] for d in documentation_facts(element, by_id))
            binding = mapped[key]
            if group == 'requirements' and 'requirementId' in binding:
                sem = element.get('semantics', {})
                if sem.get('reqId') != key or docs.strip() != binding.get('statement', '').strip():
                    issue('native-requirement-fields', key, 'Requirement ID or obligation text differs from the authored record.')
                comments = [by_id.get(ref['id'], {}) for ref in references(sem.get('ownedElement'))]
                docs = '\n'.join(
                    item.get('semantics', {}).get('body', '') for item in comments
                    if item.get('metaclass') == 'Comment' and item.get('name') == 'ReviewBasis')
            if group == 'stateMachines' and not docs:
                for typ in references(element.get('semantics', {}).get('type')):
                    docs += '\n'.join(d['body'] for d in documentation_facts(by_id.get(typ['id'], {}), by_id))
            marker = 'Basis: ' + record.get('basis', '') + '; status: ' + record.get('status', '') + '.'
            if marker not in docs or any('Source: ' + s not in docs for s in record.get('sourceRefs', [])):
                issue('native-assertion-metadata', key, 'Native documentation lost the authored basis, status or source locator.')
            if record.get('acceptanceEvidence') and 'Acceptance evidence: ' + json.dumps(record['acceptanceEvidence'], ensure_ascii=False, sort_keys=True) not in docs:
                issue('native-acceptance-evidence', key, 'Native documentation lost the identified acceptance evidence; modeled status alone is insufficient.')

    def paths_for(element, field):
        return [p for v in references(element.get('semantics', {}).get(field))
                if (p := reference_path(v, by_id))]

    def names_for(element, field):
        return [p[-1] for p in paths_for(element, field)]

    def node(ref):
        return by_id.get(ref.get('id'), {}) if isinstance(ref, dict) else {}

    def target_name(key):
        return resolved.get(key, {}).get('qualifiedName')

    def matches_endpoint(element, field, expected, key, code):
        actual = names_for(element, field)
        if not expected or actual != [expected]:
            issue(code, key, 'Resolved ' + field + ' differs from the authored endpoint.')
            return False
        return True

    # Use explicit engine ownership and performedAction, never the role caption.
    for activity in packet.get('operationalActivities', []):
        if activity['id'] not in resolved: continue
        actor = target_name(activity.get('performer'))
        candidates = [e for e in by_owner.get(actor, []) if e['metaclass'] == 'PerformActionUsage'
                      and names_for(e, 'performedAction') == [target_name(activity['id'])]]
        if len(candidates) != 1:
            issue('native-operational-performer', activity['id'], 'Expected one actor-owned performance of the actual operational activity usage.')
        else:
            relations.append(dict(kind='performance', source=actor, target=target_name(activity['id'])))
    for group in ('functions', 'operationalActivities', 'logicalComponents'):
        for record in packet.get(group, []):
            if record['id'] in resolved and record.get('parent'):
                matches_endpoint(resolved[record['id']], 'owner', target_name(record['parent']), record['id'], 'native-decomposition')

    dependencies = [e for e in report.get('elements', []) if e['metaclass'] == 'Dependency']
    for function in packet.get('functions', []):
        for activity in function.get('realizes', []):
            pair = (target_name(function['id']), target_name(activity))
            if not all(pair) or not any(names_for(d, 'client') == [pair[0]] and names_for(d, 'supplier') == [pair[1]] for d in dependencies):
                issue('native-operational-trace', function['id'], 'No resolved function-to-operational-activity dependency matches ' + activity + '.')
            else:
                relations.append(dict(kind='operational-trace', source=pair[0], target=pair[1]))

    for exchange in packet.get('exchanges', []):
        e = resolved.get(exchange['id'])
        if not e: continue
        binding = mapped[exchange['id']]
        for field, key in [('source', 'source'), ('target', 'target')]:
            matches_endpoint(e, field, target_name(exchange[key]), exchange['id'], 'native-exchange-endpoint')
        payload_types = []
        for field, bound_field, direction in [('sourceOutputFeature', 'sourceOutput', 'out'), ('targetInputFeature', 'targetInput', 'in')]:
            endpoint = node(e.get('semantics', {}).get(field))
            redefined = [n for r in references(endpoint.get('semantics', {}).get('ownedRedefinition'))
                         for n in names_for(node(r), 'redefinedFeature')]
            expected_end = binding.get(bound_field)
            if not expected_end or redefined != [expected_end]:
                issue('native-exchange-payload-end', exchange['id'], 'Resolved ' + field + ' does not redefine the bound function parameter.')
            declared = by_name.get(expected_end, [])
            types = names_for(endpoint, 'type')
            if len(declared) != 1 or not types or types != names_for(declared[0], 'type') or declared[0].get('semantics', {}).get('direction') != direction:
                issue('native-exchange-payload-type', exchange['id'], 'Flow parameter type/direction differs from its function signature.')
            payload_types.append(set(types))
        if payload_types[0] != payload_types[1]:
            issue('native-exchange-type-incompatibility', exchange['id'], 'This bounded profile requires the same declared payload type at both ends.')
        relations.append(dict(id=exchange['id'], kind='functional-exchange', source=target_name(exchange['source']),
                              target=target_name(exchange['target']), payloadTypes=sorted(payload_types[0])))
    for allocation in packet.get('allocations', []):
        e = resolved.get(allocation['id'])
        if not e: continue
        for field, key in [('source', 'function'), ('target', 'component')]:
            matches_endpoint(e, field, target_name(allocation[key]), allocation['id'], 'native-allocation-endpoint')
        relations.append(dict(id=allocation['id'], kind='allocation', source=target_name(allocation['function']), target=target_name(allocation['component'])))
    primary = {a['function']: a['component'] for a in packet.get('allocations', [])}
    for exchange in packet.get('exchanges', []):
        source_component, target_component = primary.get(exchange['source']), primary.get(exchange['target'])
        if not source_component or not target_component or source_component == target_component:
            continue
        binding = bindings.get('interfaces', {}).get(exchange['id'], {})
        interface = locate(exchange['id'] + ':interface', {'InterfaceUsage'}, binding.get('qualifiedName'))
        if not interface: continue
        for field, component, port in [('sourceFeature', source_component, 'sourcePort'), ('targetFeature', target_component, 'targetPort')]:
            paths = paths_for(interface, field)
            if (len(paths) != 1 or len(paths[0]) < 2 or paths[0][-1] != binding.get(port)
                    or paths[0][-2] != target_name(component)):
                issue('native-interface-endpoint', exchange['id'], 'Logical interface does not connect the actual allocated component port.')
        interface_types = [node(t) for t in references(interface.get('semantics', {}).get('type'))]
        flows = [node(c) for typ in interface_types for c in references(typ.get('semantics', {}).get('ownedElement')) if node(c).get('metaclass') == 'FlowUsage']
        if len(flows) != 1 or names_for(flows[0], 'payloadType') != [binding.get('payloadType')]:
            issue('native-interface-payload', exchange['id'], 'Logical interface contract does not carry the bound functional payload type.')
        if names_for(resolved.get(exchange['id'], {}), 'payloadType') != [binding.get('payloadType')]:
            issue('native-interface-functional-payload', exchange['id'], 'Logical interface payload differs from the functional exchange it implements.')
        relations.append(dict(id=exchange['id'] + ':interface', kind='logical-interface',
                              source=target_name(source_component), target=target_name(target_component), payloadType=binding.get('payloadType')))
    for exchange in packet.get('contextExchanges', []):
        interface = resolved.get(exchange['id'])
        if not interface: continue
        binding = mapped[exchange['id']]
        for field, key, port in [('sourceFeature', 'source', 'sourcePort'), ('targetFeature', 'target', 'targetPort')]:
            paths = paths_for(interface, field)
            if (len(paths) != 1 or len(paths[0]) < 2 or paths[0][-1] != binding.get(port)
                    or paths[0][-2] != target_name(exchange[key])):
                issue('native-context-endpoint', exchange['id'], 'Context interface does not connect the declared actor/component port occurrence.')
            declared = by_name.get(binding.get(port), [])
            if len(declared) != 1 or declared[0]['metaclass'] != 'PortUsage' or not names_for(declared[0], 'type'):
                issue('native-context-port-type', exchange['id'], 'Context endpoint does not resolve to a typed native port.')
        interface_types = [node(t) for t in references(interface.get('semantics', {}).get('type'))]
        flows = [node(c) for typ in interface_types for c in references(typ.get('semantics', {}).get('ownedElement')) if node(c).get('metaclass') == 'FlowUsage']
        if len(flows) != 1 or names_for(flows[0], 'payloadType') != [binding.get('payloadType')]:
            issue('native-context-payload', exchange['id'], 'Context interface does not carry the declared payload type.')
        relations.append(dict(id=exchange['id'], kind='context-interface', source=target_name(exchange['source']),
                              target=target_name(exchange['target']), payloadType=binding.get('payloadType')))
    for requirement in packet.get('requirements', []):
        e = resolved.get(requirement['id'])
        if not e: continue
        sem = e.get('semantics', {})
        if not sem.get('subjectParameter') or not sem.get('requiredConstraint'):
            issue('native-requirement-structure', requirement['id'], 'Native requirement needs an explicit subject and required constraint; documentation alone is insufficient.')
        subject = node(sem.get('subjectParameter'))
        values = [node(m) for m in references(subject.get('semantics', {}).get('ownedMembership'))
                  if node(m).get('metaclass') == 'FeatureValue'
                  and node(m).get('semantics', {}).get('featureWithValue', {}).get('id') == subject.get('sessionElementId')]
        paths = [expression_fact(node(v.get('semantics', {}).get('value')), by_id) for v in values]
        desired = target_name(requirement['subject'])
        if len(paths) != 1 or paths[0].get('kind') != 'FeaturePath' or not paths[0].get('path') or paths[0]['path'][-1] != desired:
            issue('native-requirement-subject', requirement['id'], 'Requirement subject is not bound to the authored function/component occurrence.')
        constraints = [node(c) for c in references(sem.get('requiredConstraint'))]
        if not constraints or any(constraint_membership_kind(c, by_id) != 'requirement' for c in constraints):
            issue('native-requirement-polarity', requirement['id'], 'Criterion must resolve through a required-constraint membership.')
        if requirement.get('formalConstraint'):
            formal = requirement['formalConstraint']
            expressions = [expression_fact(c, by_id) for c in constraints]
            top = expressions[0] if len(expressions) == 1 else {}
            if not formal_constraint_matches(top, formal, subject.get('qualifiedName'), mapped[requirement['id']].get('formalAttribute')):
                issue('native-formal-criterion', requirement['id'], 'Resolved subject attribute, comparison, bound or unit differs from the authored formal criterion.')
        elif not any(requirement.get('criterion', '') in d['body'] for c in constraints for d in documentation_facts(c, by_id)):
            issue('native-qualitative-criterion', requirement['id'], 'Required constraint lost the authored qualitative criterion.')
        relations.append(dict(id=requirement['id'], kind='requirement-subject', target=desired,
                              criterionMode='formal-expression' if requirement.get('formalConstraint') else 'documented-qualitative-criterion'))
    for case in packet.get('verificationCases', []):
        e = resolved.get(case['id'])
        if not e: continue
        actual = set(names_for(e, 'verifiedRequirement'))
        expected = {target_name(r) for r in case['requirementIds']}
        if None in expected or actual != expected:
            issue('native-verification-target', case['id'], 'Native verification objective must target the authored requirements.')
        relations.append(dict(id=case['id'], kind='planned-verification', targets=sorted(n for n in actual if n)))

    for scenario in packet.get('scenarios', []):
        parent = target_name(scenario['id']); steps, control_endpoints, allowed_links = {}, {}, set()
        for step in scenario.get('steps', []):
            key = scenario['id'] + '/' + step['id']
            e = locate(key, {'ActionUsage'})
            if e:
                steps[step['id']] = e
                matches_endpoint(e, 'owner', parent, key, 'native-scenario-owner')
                actual_type = names_for(e, 'type')
                if not actual_type or actual_type != names_for(resolved.get(step['function'], {}), 'type'):
                    issue('native-scenario-function', key, 'Step does not use the authored function type.')
        direct = by_owner.get(parent, [])
        entry = scenario.get('entryStep', scenario['steps'][0]['id'])
        starts = [e for e in direct if e['metaclass'] == 'SuccessionAsUsage'
                  and names_for(e, 'sourceFeature') == ['Actions::Action::start']
                  and names_for(e, 'targetFeature') == [steps.get(entry, {}).get('qualifiedName')]]
        if len(starts) != 1:
            issue('native-scenario-entry', scenario['id'], 'Native start does not enter the declared first step.')
        allowed_links.update(e['sessionElementId'] for e in starts)
        for group in scenario.get('parallelGroups', []):
            gid = scenario['id'] + '/' + group['id']
            binding = bindings.get('parallelGroups', {}).get(gid, {})
            fork = locate(gid + '/fork', {'ForkNode'}, binding.get('fork'))
            join = locate(gid + '/join', {'JoinNode'}, binding.get('join'))
            if not fork or not join: continue
            fork_name, join_name = fork['qualifiedName'], join['qualifiedName']
            for control in (fork, join):
                matches_endpoint(control, 'owner', parent, gid, 'native-parallel-owner')
            branches_out = [t for t in scenario['transitions'] if t['from'] == group['from'] and t['to'] in group['branches'] and t.get('kind') == 'parallel']
            joins_in = [t for t in scenario['transitions'] if t['to'] == group['join'] and t.get('kind') == 'join']
            if (binding.get('scenarioId') != scenario['id'] or binding.get('fromId') != group['from']
                    or binding.get('branchIds') != group['branches'] or binding.get('joinStepId') != group['join']
                    or set(binding.get('branchTransitionIds', [])) != {t['id'] for t in branches_out}
                    or set(binding.get('joinTransitionIds', [])) != {t['id'] for t in joins_in}):
                issue('native-parallel-binding', gid, 'Bound control group differs from the declared concurrent obligations.')
            for link, source, target in [('entryLink', steps.get(group['from'], {}).get('qualifiedName'), fork_name),
                                          ('exitLink', join_name, steps.get(group['join'], {}).get('qualifiedName'))]:
                e = locate(gid + '/' + link, {'SuccessionAsUsage'}, binding.get(link))
                if e:
                    allowed_links.add(e['sessionElementId'])
                    matches_endpoint(e, 'owner', parent, gid, 'native-parallel-owner')
                    matches_endpoint(e, 'sourceFeature', source, gid, 'native-parallel-control')
                    matches_endpoint(e, 'targetFeature', target, gid, 'native-parallel-control')
            for t in branches_out:
                control_endpoints[t['id']] = (fork_name, steps.get(t['to'], {}).get('qualifiedName'))
            for t in joins_in:
                control_endpoints[t['id']] = (steps.get(t['from'], {}).get('qualifiedName'), join_name)
            relations.append(dict(id=gid, kind='parallel-obligations', fork=fork_name, join=join_name,
                                  branches=[steps.get(b, {}).get('qualifiedName') for b in group['branches']]))
        for transition in scenario.get('transitions', []):
            mc = 'TransitionUsage' if transition.get('condition') else 'SuccessionAsUsage'
            e = locate(transition['id'], {mc})
            if not e: continue
            allowed_links.add(e['sessionElementId'])
            matches_endpoint(e, 'owner', parent, transition['id'], 'native-scenario-owner')
            authored_ends = (steps.get(transition['from'], {}).get('qualifiedName'), steps.get(transition['to'], {}).get('qualifiedName'))
            expected_ends = control_endpoints.get(transition['id'], authored_ends)
            for field, end in zip(('source', 'target'), expected_ends):
                native_field = field if mc == 'TransitionUsage' else field + 'Feature'
                matches_endpoint(e, native_field, end, transition['id'], 'native-scenario-endpoint')
            if transition.get('condition') and not references(e.get('semantics', {}).get('guardExpression')):
                issue('native-scenario-guard', transition['id'], 'A documented branch condition has no native guard expression.')
            relations.append(dict(id=transition['id'], kind='scenario-transition', source=expected_ends[0], target=expected_ends[1]))
        outgoing = {t['from'] for t in scenario.get('transitions', [])}
        exits = scenario.get('exitSteps', [s for s in steps if s not in outgoing])
        for end in exits:
            guarded = bool(scenario.get('exitGuards', {}).get(end))
            mc, sf, tf = ('TransitionUsage', 'source', 'target') if guarded else ('SuccessionAsUsage', 'sourceFeature', 'targetFeature')
            candidates = [e for e in direct if e['metaclass'] == mc
                          and names_for(e, sf) == [steps.get(end, {}).get('qualifiedName')]
                          and names_for(e, tf) == ['Actions::Action::done']]
            if len(candidates) != 1 or (guarded and not candidates[0].get('semantics', {}).get('guardExpression')):
                issue('native-scenario-exit', scenario['id'] + '/' + end, 'Native completion/guard does not match the declared terminal outcome.')
            allowed_links.update(e['sessionElementId'] for e in candidates)
        for e in direct:
            if e['metaclass'] in ('TransitionUsage', 'SuccessionAsUsage') and e['sessionElementId'] not in allowed_links:
                issue('native-unmodeled-scenario-link', scenario['id'], 'An undeclared native control link could skip or add a scenario obligation.')

    for state in packet.get('stateMachines', []):
        e = resolved.get(state['id'])
        if not e: continue
        binding = mapped[state['id']]
        matches_endpoint(e, 'owner', target_name(state['subject']), state['id'], 'native-state-subject')
        definition_name = binding.get('definition')
        definition = locate(state['id'] + ':definition', {'StateDefinition'}, definition_name)
        if not definition or names_for(e, 'type') != [definition_name]:
            issue('native-state-definition', state['id'], 'State occurrence does not use its bound state definition.'); continue
        state_names = binding.get('states', {})
        for s in state.get('states', []):
            child = locate(state['id'] + '/' + s['id'], {'StateUsage'}, state_names.get(s['id']))
            if child: matches_endpoint(child, 'owner', definition_name, state['id'], 'native-state-owner')
        initial = state.get('initial', state['states'][0]['id'])
        entry_action = names_for(definition, 'entryAction')
        initial_edges = [c for c in by_owner.get(definition_name, []) if c['metaclass'] == 'SuccessionAsUsage'
                         and names_for(c, 'sourceFeature') == entry_action
                         and names_for(c, 'targetFeature') == [state_names.get(initial)]]
        if not entry_action or len(initial_edges) != 1:
            issue('native-state-entry', state['id'], 'State entry does not enter the declared initial state.')
        for transition in state.get('transitions', []):
            key = state['id'] + '/' + transition['id']
            child = locate(key, {'TransitionUsage'}, binding.get('transitions', {}).get(transition['id']))
            if not child: continue
            for field, key_name in [('source', 'from'), ('target', 'to')]:
                matches_endpoint(child, field, state_names.get(transition[key_name]), key, 'native-state-endpoint')
            for authored, native in [('guard', 'guardExpression'), ('event', 'triggerAction')]:
                if transition.get(authored) and not references(child.get('semantics', {}).get(native)):
                    issue('native-state-' + authored, key, 'Authored ' + authored + ' lacks its native relation.')
            relations.append(dict(id=key, kind='state-transition', source=state_names.get(transition['from']), target=state_names.get(transition['to']), effectEvidence='documented-obligation'))
        declared_terminals = state.get('terminalStates', [])
        terminal_bindings = binding.get('terminalTransitions', {})
        if set(terminal_bindings) != set(declared_terminals):
            issue('native-state-terminal-binding', state['id'], 'Completion bindings differ from declared terminal states.')
        terminal_ids = set()
        for terminal in declared_terminals:
            key = state['id'] + '/terminal:' + terminal
            child = locate(key, {'TransitionUsage'}, terminal_bindings.get(terminal))
            if not child: continue
            terminal_ids.add(child['sessionElementId'])
            matches_endpoint(child, 'owner', definition_name, key, 'native-state-owner')
            matches_endpoint(child, 'source', state_names.get(terminal), key, 'native-state-terminal')
            matches_endpoint(child, 'target', 'States::StateAction::done', key, 'native-state-terminal')
            relations.append(dict(id=key, kind='state-completion', source=state_names.get(terminal), target='States::StateAction::done'))
        for child in by_owner.get(definition_name, []):
            if (child['metaclass'] == 'TransitionUsage' and names_for(child, 'target') == ['States::StateAction::done']
                    and child['sessionElementId'] not in terminal_ids):
                issue('native-undeclared-state-completion', state['id'], 'An undeclared native completion changes the authored lifecycle policy.')
        if state.get('terminalPolicy') == 'ongoing':
            docs = '\n'.join(d['body'] for d in documentation_facts(definition, by_id))
            if 'Lifecycle policy: ongoing' not in docs or state.get('lifecycleExitCondition', '') not in docs:
                issue('native-state-lifecycle-policy', state['id'], 'Ongoing lifecycle policy/exit obligation was not retained.')

    expected = bindings.get('expected')
    facts = None
    try:
        facts = check_contract(report, expected)
        if not facts['passed']:
            issue('native-expected-facts', 'bindings', 'One or more independent expected native facts do not match.')
    except (ValueError, KeyError, TypeError) as error:
        issue('native-expected-contract', 'bindings', str(error))
    return {'passed': not issues, 'issues': issues, 'expectedFacts': facts,
            'normalizedRelations': relations,
            'nativeProjectionScope': list(NATIVE_KINDS),
            'annotationsOnly': ['parameters', 'insights', 'decisions'],
            'limits': 'Resolved native identity and relationship checks plus retained assertion metadata; no source entailment, guard evaluation, engineering acceptance or behavior execution.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--model', type=Path)
    parser.add_argument('--native-report', type=Path)
    parser.add_argument('--bindings', type=Path)
    parser.add_argument('--require-ready', action='store_true')
    args = parser.parse_args(argv)
    if args.output.resolve() in {path.resolve() for path in (args.architecture, args.model, args.native_report, args.bindings) if path}:
        parser.error('Output must not overwrite an authored or native input.')
    raw = args.architecture.read_bytes()
    packet = json.loads(raw)
    result = check_architecture(packet)
    result['architectureSha256'] = hashlib.sha256(raw).hexdigest()
    if any((args.model, args.native_report, args.bindings)):
        if not all((args.model, args.native_report, args.bindings)):
            parser.error('Native assessment needs --model, --native-report and --bindings together.')
        from report_integrity import load_report
        try:
            report = load_report(args.native_report, source=args.model)
            binding_bytes = args.bindings.read_bytes()
            result['modelSha256'] = hashlib.sha256(args.model.read_bytes()).hexdigest()
            result['bindingsSha256'] = hashlib.sha256(binding_bytes).hexdigest()
            result['nativeReportSha256'] = hashlib.sha256(args.native_report.read_bytes()).hexdigest()
            native = check_native_bindings(packet, report, json.loads(binding_bytes))
            result['nativeValidation'] = 'managed-report-and-facts-checked' if native['passed'] else 'failed'
            result['native'] = native
            if not native['passed']:
                result['structuralConsistencyPassed'] = False
                result['reviewReadiness'] = 'invalid'
                result['errorCount'] = result.get('errorCount', 0) + len(native['issues'])
        except (ValueError, OSError, KeyError, TypeError) as error:
            result['nativeValidation'] = 'failed'
            result['native'] = {'passed': False, 'error': str(error)}
            result['structuralConsistencyPassed'] = False
            result['reviewReadiness'] = 'invalid'
            result['errorCount'] = result.get('errorCount', 0) + 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: result.get(k) for k in ('reviewReadiness', 'errorCount', 'reviewItemCount', 'nativeValidation')}))
    return 2 if not result['structuralConsistencyPassed'] or (args.require_ready and result['reviewReadiness'] != 'candidate-ready-for-engineering-review') else 0


if __name__ == '__main__':
    raise SystemExit(main())
