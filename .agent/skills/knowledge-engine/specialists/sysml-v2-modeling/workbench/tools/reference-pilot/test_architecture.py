"""Independent defect fixtures for architecture sufficiency and native relations.

The small example is deliberately unrelated to the airport recipe. Native facts
are authored independently of architecture_model.py; mutations retain names and
counts, so a catalogue/count-only acceptance implementation cannot pass them.
"""
import copy
import hashlib
import json
import unittest

from architecture_check import check_architecture, check_native_bindings, formal_constraint_matches


def record(key, **fields):
    return dict(id=key, label=key, description='Review example.', basis='derived',
                sourceRefs=['brief:section-1'], status='proposed', **fields)


def recipe():
    packet = dict(schemaVersion=1, scope=dict(name='Sample handling',
        boundary='Operator and sample-handling service.', included=['Sample decisions'],
        excluded=['Physical design'], phase='Candidate logical architecture',
        decision='Agree handoff and failure handling.', requiredScenarioKinds=['nominal']))
    packet.update(
        actors=[record('operator')],
        operationalActivities=[record('handle', performer='operator')],
        functions=[record('read', level='system', realizes=['handle']),
                   record('choose', level='system', realizes=['handle'])],
        exchanges=[record('sample', source='read', target='choose', item='Sample record',
                          condition='Read complete', kind='data')],
        logicalComponents=[record('service')],
        allocations=[record('read-allocation', function='read', component='service', rationale='Own sampling.'),
                     record('choose-allocation', function='choose', component='service', rationale='Own decision.')],
        scenarios=[record('normal', kind='nominal', entryStep='r', exitSteps=['c'],
                          entryConditions=['Sample available'], exitConditions=['Decision recorded'],
                          steps=[dict(id='r', function='read', actor='operator'), dict(id='c', function='choose')],
                          transitions=[dict(id='next', **{'from': 'r', 'to': 'c'}, condition='Sample read')])],
        requirements=[record('decision', subject='choose', condition='When a valid sample is supplied',
                             criterion='The decision identifies the sample and assigned handling route.',
                             rationale='Preserve accountable disposition.', derivedFrom=['handle'], verificationIds=['review'])],
        verificationCases=[dict(record('review', requirementIds=['decision'], method='Inspection',
                                       setup='Use a labeled sample and a missing-label sample.',
                                       expectedResult='Each case has a route or explicit unresolved disposition.'), status='planned')],
        decisions=[], stateMachines=[], insights=[], coverage={'brief:section-1': ['handle', 'decision']})
    return packet


def native_fixture():
    p = recipe()
    elements, by_key = [], {}

    def element(key, metaclass, qn=None, **sem):
        e = dict(sessionElementId=key, metaclass=metaclass, semantics=sem)
        if qn:
            e['qualifiedName'] = qn
            e['name'] = qn.rsplit('::', 1)[-1]
        elements.append(e); by_key[key] = e
        return e

    def ref(e):
        return dict(id=e['sessionElementId'], metaclass=e['metaclass'],
                    **({'qualifiedName': e['qualifiedName']} if e.get('qualifiedName') else {}))

    def documented(e, r, body=None):
        body = body or ('Basis: ' + r['basis'] + '; status: ' + r['status'] + '.\n'
                        + '\n'.join('Source: ' + s for s in r['sourceRefs']))
        d = element(e['sessionElementId'] + '-doc', 'Documentation', body=body,
                    owner=ref(e), documentedElement=ref(e))
        e['semantics']['documentation'] = [ref(d)]

    mapped = {}
    kinds = {'actors': 'PartUsage', 'operationalActivities': 'ActionUsage', 'functions': 'ActionUsage',
             'exchanges': 'FlowUsage', 'logicalComponents': 'PartUsage', 'allocations': 'AllocationUsage',
             'scenarios': 'ActionUsage', 'requirements': 'RequirementUsage', 'verificationCases': 'VerificationCaseDefinition'}
    for group, kind in kinds.items():
        for r in p[group]:
            # Arbitrary native names ensure no hidden dependence on emitter names.
            e = element(r['id'], kind, 'Independent::native_' + str(len(elements)))
            documented(e, r)
            mapped[r['id']] = dict(qualifiedName=e['qualifiedName'], metaclass=kind)
    for key in ('read', 'choose'):
        typ = element('type-' + key, 'ActionDefinition', 'Independent::Type_' + key)
        by_key[key]['semantics']['type'] = [ref(typ)]
        element('trace-' + key, 'Dependency', client=[ref(by_key[key])], supplier=[ref(by_key['handle'])])
    element('perform', 'PerformActionUsage', owner=ref(by_key['operator']), performedAction=ref(by_key['handle']))
    payload = element('payload', 'ItemDefinition', 'Independent::Sample')
    flow = by_key['sample']
    for field, key, direction in [('source', 'read', 'out'), ('target', 'choose', 'in')]:
        formal = element('parameter-' + field, 'ItemUsage', 'Independent::Type_' + key + '::record', type=[ref(payload)], direction=direction)
        end = element('end-' + field, 'ReferenceUsage', type=[ref(payload)])
        redef = element('redef-' + field, 'Redefinition', redefinedFeature=ref(formal))
        end['semantics']['ownedRedefinition'] = [ref(redef)]
        flow['semantics'][field] = [ref(by_key[key])]
        flow['semantics']['sourceOutputFeature' if field == 'source' else 'targetInputFeature'] = ref(end)
        mapped['sample']['sourceOutput' if field == 'source' else 'targetInput'] = formal['qualifiedName']
    for key in ('read', 'choose'):
        by_key[key + '-allocation']['semantics'].update(source=[ref(by_key[key])], target=[ref(by_key['service'])])
    requirement = by_key['decision']
    subject = element('subject', 'ReferenceUsage', requirement['qualifiedName'] + '::subject')
    expression = element('subject-expression', 'FeatureReferenceExpression', referent=ref(by_key['choose']))
    value = element('subject-value', 'FeatureValue', featureWithValue=ref(subject), value=ref(expression))
    subject['semantics']['ownedMembership'] = [ref(value)]
    criterion = element('criterion', 'ConstraintUsage', requirement['qualifiedName'] + '::criterion')
    membership = element('criterion-membership', 'RequirementConstraintMembership', kind='requirement', ownedConstraint=ref(criterion))
    criterion['semantics']['owningMembership'] = ref(membership)
    documented(criterion, p['requirements'][0], p['requirements'][0]['criterion'])
    requirement['semantics'].update(subjectParameter=ref(subject), requiredConstraint=[ref(criterion)])
    by_key['review']['semantics']['verifiedRequirement'] = [ref(requirement)]
    parent = by_key['normal']
    steps = {}
    for key, function in [('r', 'read'), ('c', 'choose')]:
        e = element('step-' + key, 'ActionUsage', parent['qualifiedName'] + '::' + key,
                    owner=ref(parent), type=by_key[function]['semantics']['type'])
        mapped['normal/' + key] = dict(qualifiedName=e['qualifiedName'], metaclass='ActionUsage')
        steps[key] = e
    start = dict(id='start', qualifiedName='Actions::Action::start')
    done = dict(id='done', qualifiedName='Actions::Action::done')
    element('entry', 'SuccessionAsUsage', owner=ref(parent), sourceFeature=start, targetFeature=[ref(steps['r'])])
    guard = element('guard', 'FeatureReferenceExpression')
    transition = element('next', 'TransitionUsage', parent['qualifiedName'] + '::next', owner=ref(parent),
                         source=ref(steps['r']), target=ref(steps['c']), guardExpression=ref(guard))
    mapped['next'] = dict(qualifiedName=transition['qualifiedName'], metaclass='TransitionUsage')
    element('exit', 'SuccessionAsUsage', owner=ref(parent), sourceFeature=ref(steps['c']), targetFeature=[done])
    digest = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    bindings = dict(schemaVersion=1, modelSha256='a' * 64, recipeSha256=digest, elements=mapped,
                    expected=dict(schemaVersion=1, checks=[dict(id='one-independent-selector', select=dict(qualifiedName=parent['qualifiedName']), expect=dict(metaclass='ActionUsage'))]))
    return p, dict(staticChecksPassed=True, sourceSha256='a' * 64, elements=elements), bindings, by_key


def concurrent_native_fixture():
    p, report, bindings, index = native_fixture()
    s = p['scenarios'][0]
    s['steps'] += [dict(id='b1', function='read'), dict(id='b2', function='choose')]
    s['parallelGroups'] = [dict(id='both', **{'from': 'r'}, branches=['b1', 'b2'], join='c')]
    s['transitions'] = [dict(id=key, **{'from': source, 'to': target}, kind=kind, condition=condition)
        for key, source, target, kind, condition in [
            ('next', 'r', 'b1', 'parallel', 'Case requires both obligations'),
            ('branch-two', 'r', 'b2', 'parallel', 'Case requires both obligations'),
            ('join-one', 'b1', 'c', 'join', 'Reading complete'),
            ('join-two', 'b2', 'c', 'join', 'Decision complete')]]
    parent = index['normal']; qn = parent['qualifiedName']

    def ref(key):
        e = index[key]
        return dict(id=e['sessionElementId'], qualifiedName=e.get('qualifiedName'))

    def add(key, mc, suffix, **sem):
        e = dict(sessionElementId=key, metaclass=mc, qualifiedName=qn + '::' + suffix, semantics=dict(owner=ref('normal'), **sem))
        report['elements'].append(e); index[key] = e
        return e

    for key, function in [('b1', 'read'), ('b2', 'choose')]:
        step = add('step-' + key, 'ActionUsage', key, type=index[function]['semantics']['type'])
        bindings['elements']['normal/' + key] = dict(qualifiedName=step['qualifiedName'], metaclass='ActionUsage')
    fork = add('fork', 'ForkNode', 'fork_in_native')
    join = add('join', 'JoinNode', 'join_in_native')
    enter = add('fork-enter', 'SuccessionAsUsage', 'enter_control', sourceFeature=ref('step-r'), targetFeature=[ref('fork')])
    leave = add('join-leave', 'SuccessionAsUsage', 'leave_control', sourceFeature=ref('join'), targetFeature=[ref('step-c')])
    for key, source, target in [('next', 'fork', 'step-b1'), ('branch-two', 'fork', 'step-b2'), ('join-one', 'step-b1', 'join'), ('join-two', 'step-b2', 'join')]:
        if key == 'next':
            index[key]['semantics'].update(source=ref(source), target=ref(target))
            e = index[key]
        else:
            e = add(key, 'TransitionUsage', key, source=ref(source), target=ref(target), guardExpression=ref('guard'))
        bindings['elements'][key] = dict(qualifiedName=e['qualifiedName'], metaclass='TransitionUsage')
    bindings['parallelGroups'] = {'normal/both': dict(scenarioId='normal', fork=fork['qualifiedName'], join=join['qualifiedName'],
        fromId='r', branchIds=['b1', 'b2'], joinStepId='c', branchTransitionIds=['next', 'branch-two'],
        joinTransitionIds=['join-one', 'join-two'], entryLink=enter['qualifiedName'], exitLink=leave['qualifiedName'])}
    bindings['recipeSha256'] = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    return p, report, bindings, index


class ArchitectureReviewTests(unittest.TestCase):
    def assert_issue(self, packet, code, severity=None):
        result = check_architecture(packet)
        self.assertTrue(any(i['code'] == code and (severity is None or i['severity'] == severity) for i in result['issues']), result)
        return result

    def test_connected_review_candidate_does_not_claim_native_or_acceptance(self):
        result = check_architecture(recipe())
        self.assertEqual(result['reviewReadiness'], 'candidate-ready-for-engineering-review')
        self.assertEqual(result['nativeValidation'], 'not-assessed')
        self.assertEqual(result['engineeringAcceptance'], 'not-assessed')

    def test_definition_catalogue_is_not_architecture(self):
        p = recipe(); p['functions'] = []; p['exchanges'] = []
        self.assert_issue(p, 'architecture-empty', 'error')

    def test_relationship_endpoints_must_be_declared_and_typed(self):
        for key, value, code in [('component', 'missing', 'unresolved-reference'), ('component', 'read', 'wrong-reference-kind')]:
            p = recipe(); p['allocations'][0][key] = value
            self.assert_issue(p, code, 'error')

    def test_disconnected_function_and_missing_allocation_remain_open(self):
        p = recipe(); p['functions'].append(record('orphan', realizes=['handle']))
        r = self.assert_issue(p, 'disconnected-function', 'review')
        self.assertTrue(r['structuralConsistencyPassed'])
        self.assertEqual(r['reviewReadiness'], 'review-required')
        self.assert_issue(p, 'unallocated-function', 'review')

    def test_requirement_criterion_and_plan_are_not_optional_completion(self):
        p = recipe(); p['requirements'][0]['criterion'] = 'TBD'; p['verificationCases'][0]['setup'] = ''
        self.assert_issue(p, 'undefined-requirement-criterion', 'review')
        self.assert_issue(p, 'incomplete-verification-plan', 'review')

    def test_open_decision_is_not_silently_passed(self):
        p = recipe(); p['decisions'] = [record('decision-open', affects=['choose'], question='Who decides?', options=['Operator', 'Service'])]
        r = self.assert_issue(p, 'unresolved-decision', 'review')
        self.assertEqual(r['reviewReadiness'], 'review-required')

    def test_missing_failure_scenario_is_scope_specific_review_item(self):
        p = recipe(); p['scope']['requiredScenarioKinds'].append('failure')
        self.assert_issue(p, 'missing-scenario-kind', 'review')

    def test_undeclared_unreachable_and_trapped_branches_are_detected(self):
        p = recipe(); p['scenarios'][0]['transitions'][0]['to'] = 'missing'
        self.assert_issue(p, 'dangling-transition', 'error')
        p = recipe(); p['scenarios'][0]['steps'].append(dict(id='unreachable', function='read'))
        self.assert_issue(p, 'unreachable-step', 'error')
        p = recipe(); p['scenarios'][0]['transitions'][0]['to'] = 'r'
        self.assert_issue(p, 'no-exit-path', 'review')

    def test_planned_verification_is_distinct_from_results(self):
        p = recipe(); p['verificationCases'][0]['actualResult'] = 'passed'
        self.assert_issue(p, 'verification-result-in-plan', 'error')
        p = recipe(); p['verificationCases'][0]['status'] = 'passed'
        self.assert_issue(p, 'verification-not-planned', 'error')
        p = recipe(); p['verificationCases'][0]['passed'] = False
        self.assert_issue(p, 'verification-result-in-plan', 'error')

    def test_proposal_is_not_a_source_assertion(self):
        p = recipe(); p['functions'][0].update(basis='proposed', sourceRefs=[])
        self.assertTrue(check_architecture(p)['structuralConsistencyPassed'])
        p['functions'][0]['basis'] = 'source-explicit'
        self.assert_issue(p, 'uncited-source-claim', 'error')

    def test_states_need_reachable_lifecycle_or_terminal_disposition(self):
        p = recipe(); p['stateMachines'] = [record('lifecycle', subject='service', initial='waiting', states=[dict(id='waiting', label='Waiting'), dict(id='ready', label='Ready')],
            transitions=[dict(id='ready-now', **{'from': 'waiting', 'to': 'ready'}, event='Sample arrives', guard='Sample valid'), dict(id='reset', **{'from': 'ready', 'to': 'waiting'}, event='Completed', guard='Next sample')])]
        self.assert_issue(p, 'scenario-exit', 'review')
        p['stateMachines'][0].update(terminalPolicy='ongoing', lifecycleExitCondition='Stop service when operator closes the session.')
        self.assertTrue(check_architecture(p)['structuralConsistencyPassed'])
        self.assertFalse(any(i['code'] == 'no-exit-path' for i in check_architecture(p)['issues']))


class NativeArchitectureTests(unittest.TestCase):
    def test_declared_state_terminal_needs_native_completion(self):
        p, report, bindings, index = native_fixture()
        r = record('state', subject='service', initial='finished', terminalStates=['finished'], states=[dict(id='finished', label='Finished')], transitions=[])
        p['stateMachines'] = [r]
        def add(key, mc, qn, **sem):
            e = dict(sessionElementId=key, metaclass=mc, qualifiedName=qn, semantics=sem)
            report['elements'].append(e); index[key] = e
            return dict(id=key, qualifiedName=qn, metaclass=mc)
        definition = add('state-def', 'StateDefinition', 'Independent::Lifecycle')
        doc = add('state-doc', 'Documentation', 'Independent::Lifecycle::doc', body='Basis: derived; status: proposed.\nSource: brief:section-1', owner=definition, documentedElement=definition)
        index['state-def']['semantics']['documentation'] = [doc]
        exhibited = add('state', 'ExhibitStateUsage', 'Independent::service::lifecycle', owner=dict(id='service', qualifiedName=index['service']['qualifiedName']), type=[definition])
        finished = add('finished', 'StateUsage', 'Independent::Lifecycle::finished', owner=definition)
        entry = add('entry-action', 'ActionUsage', 'Independent::Lifecycle::entry', owner=definition)
        index['state-def']['semantics']['entryAction'] = entry
        add('state-start', 'SuccessionAsUsage', 'Independent::Lifecycle::start-edge', owner=definition, sourceFeature=entry, targetFeature=[finished])
        finish = add('state-finish', 'TransitionUsage', 'Independent::Lifecycle::finish', owner=definition, source=finished, target=dict(id='state-done', qualifiedName='States::StateAction::done'))
        bindings['elements']['state'] = dict(qualifiedName=exhibited['qualifiedName'], metaclass='ExhibitStateUsage', definition=definition['qualifiedName'], states={'finished': finished['qualifiedName']}, transitions={}, terminalTransitions={'finished': finish['qualifiedName']})
        bindings['recipeSha256'] = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        result = check_native_bindings(p, report, bindings)
        self.assertTrue(result['passed'], result['issues'])
        index['state-finish']['semantics']['target'] = finished
        result = check_native_bindings(p, report, bindings)
        self.assertFalse(result['passed'])
        self.assertIn('native-state-terminal', [i['code'] for i in result['issues']])

    def test_accepted_status_cannot_drop_its_evidence_locator(self):
        p, report, bindings, index = native_fixture()
        p['functions'][0].update(status='accepted', acceptanceEvidence={'record': 'review-17', 'scope': 'read'})
        bindings['recipeSha256'] = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
        index['read-doc']['semantics']['body'] = 'Basis: derived; status: accepted.\nSource: brief:section-1'
        result = check_native_bindings(p, report, bindings)
        self.assertFalse(result['passed'])
        self.assertIn('native-acceptance-evidence', [i['code'] for i in result['issues']])
        index['read-doc']['semantics']['body'] += '\nAcceptance evidence: ' + json.dumps(p['functions'][0]['acceptanceEvidence'], sort_keys=True)
        self.assertTrue(check_native_bindings(p, report, bindings)['passed'])

    def test_multiple_join_contributions_need_a_supported_merge(self):
        p, _, _, _ = concurrent_native_fixture()
        p['scenarios'][0]['transitions'].append(dict(id='extra-join', **{'from': 'b1', 'to': 'c'}, kind='join', condition='Alternative completion'))
        result = check_architecture(p)
        self.assertFalse(result['structuralConsistencyPassed'])
        self.assertIn('parallel-join-shape', [i['code'] for i in result['issues']])

    def test_context_contract_reconciles_actual_actor_ports_and_payload(self):
        def context_fixture():
            p, report, bindings, index = native_fixture()
            r = record('boundary', source='operator', target='service', item='Sample record', kind='data')
            p['contextExchanges'] = [r]
            def add(key, metaclass, qn, **sem):
                e = dict(sessionElementId=key, metaclass=metaclass, qualifiedName=qn, semantics=sem)
                report['elements'].append(e); index[key] = e
                return dict(id=key, qualifiedName=qn, metaclass=metaclass)
            ptype = add('port-type', 'PortDefinition', 'Independent::DataPort')
            source_port = add('source-port', 'PortUsage', 'Independent::OperatorType::out', type=[ptype])
            target_port = add('target-port', 'PortUsage', 'Independent::ServiceType::in', type=[ptype])
            source = add('context-source', 'Feature', 'Independent::sourcePath', chainingFeature=[dict(id='operator', qualifiedName=index['operator']['qualifiedName']), source_port])
            target = add('context-target', 'Feature', 'Independent::targetPath', chainingFeature=[dict(id='service', qualifiedName=index['service']['qualifiedName']), target_port])
            payload = dict(id='payload', qualifiedName=index['payload']['qualifiedName'])
            flow = add('context-flow', 'FlowUsage', 'Independent::BoundaryType::flow', payloadType=[payload])
            typ = add('context-type', 'InterfaceDefinition', 'Independent::BoundaryType', ownedElement=[flow])
            interface = add('boundary', 'InterfaceUsage', 'Independent::boundary', type=[typ], sourceFeature=source, targetFeature=[target])
            doc = add('boundary-doc', 'Documentation', 'Independent::boundary::doc', body='Basis: derived; status: proposed.\nSource: brief:section-1', owner=interface, documentedElement=interface)
            index['boundary']['semantics']['documentation'] = [doc]
            bindings['elements']['boundary'] = dict(qualifiedName=interface['qualifiedName'], metaclass='InterfaceUsage', sourcePort=source_port['qualifiedName'], targetPort=target_port['qualifiedName'], payloadType=payload['qualifiedName'])
            bindings['recipeSha256'] = hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
            return p, report, bindings, index
        p, report, bindings, _ = context_fixture()
        result = check_native_bindings(p, report, bindings)
        self.assertTrue(result['passed'], result['issues'])
        for mutation, code in [('endpoint', 'native-context-endpoint'), ('payload', 'native-context-payload')]:
            with self.subTest(mutation=mutation):
                p, report, bindings, index = context_fixture(); count = len(report['elements'])
                if mutation == 'endpoint':
                    index['context-source']['semantics']['chainingFeature'][0] = dict(id='service', qualifiedName=index['service']['qualifiedName'])
                else:
                    index['context-flow']['semantics']['payloadType'] = [dict(id='other', qualifiedName='Independent::DifferentPayload')]
                result = check_native_bindings(p, report, bindings)
                self.assertFalse(result['passed'])
                self.assertEqual(len(report['elements']), count)
                self.assertIn(code, [i['code'] for i in result['issues']])

    def test_concurrent_obligations_use_fork_and_join(self):
        p, report, bindings, _ = concurrent_native_fixture()
        self.assertTrue(check_architecture(p)['structuralConsistencyPassed'])
        result = check_native_bindings(p, report, bindings)
        self.assertTrue(result['passed'], result['issues'])

    def test_concurrency_cannot_be_replaced_with_a_choice(self):
        p, report, bindings, index = concurrent_native_fixture(); count = len(report['elements'])
        index['fork']['metaclass'] = 'DecisionNode'
        result = check_native_bindings(p, report, bindings)
        self.assertFalse(result['passed'])
        self.assertEqual(len(report['elements']), count)
        self.assertIn('native-kind-mismatch', [i['code'] for i in result['issues']])

    def test_one_obligation_cannot_bypass_the_join(self):
        p, report, bindings, index = concurrent_native_fixture(); count = len(report['elements'])
        index['join-one']['semantics']['target'] = dict(id='step-c', qualifiedName=index['step-c']['qualifiedName'])
        # A self-authored expected endpoint cannot override the authored topology.
        bindings['elements']['join-one']['nativeTarget'] = index['step-c']['qualifiedName']
        result = check_native_bindings(p, report, bindings)
        self.assertFalse(result['passed'])
        self.assertEqual(len(report['elements']), count)
        self.assertIn('native-scenario-endpoint', [i['code'] for i in result['issues']])

    def test_formal_bound_preserves_subject_operator_value_and_unit(self):
        formal = dict(attribute='storageDuration', quantity='duration', operator='>=', value=24, unit='h')
        expression = dict(kind='OperatorExpression', operator='>=', operands=[
            dict(kind='FeaturePath', path=['Req::subject', 'Service::storageDuration']),
            dict(kind='OperatorExpression', operator='[', operands=[dict(kind='LiteralInteger', value=24), dict(kind='FeaturePath', path=['SI::hour'])])])
        self.assertTrue(formal_constraint_matches(expression, formal, 'Req::subject', 'Service::storageDuration'))
        for change in ('unit', 'bound', 'operator', 'attribute'):
            wrong = copy.deepcopy(expression)
            if change == 'unit': wrong['operands'][1]['operands'][1]['path'] = ['SI::second']
            elif change == 'bound': wrong['operands'][1]['operands'][0]['value'] = 2
            elif change == 'operator': wrong['operator'] = '<='
            else: wrong['operands'][0]['path'][-1] = 'Service::unrelatedDuration'
            self.assertFalse(formal_constraint_matches(wrong, formal, 'Req::subject', 'Service::storageDuration'), change)

    def test_independently_authored_native_facts_pass(self):
        p, report, bindings, _ = native_fixture()
        result = check_native_bindings(p, report, bindings)
        self.assertTrue(result['passed'], result['issues'])
        self.assertTrue(any(r['kind'] == 'functional-exchange' for r in result['normalizedRelations']))

    def test_names_and_counts_cannot_hide_wrong_relations(self):
        mutations = {
            'native-operational-performer': lambda i: i['perform']['semantics'].update(performedAction=dict(id='read', qualifiedName=i['read']['qualifiedName'])),
            'native-operational-trace': lambda i: i['trace-read']['semantics'].update(supplier=[]),
            'native-exchange-endpoint': lambda i: i['sample']['semantics'].update(target=[dict(id='read', qualifiedName=i['read']['qualifiedName'])]),
            'native-exchange-payload-end': lambda i: i['redef-source']['semantics'].update(redefinedFeature=dict(id='parameter-target', qualifiedName=i['parameter-target']['qualifiedName'])),
            'native-allocation-endpoint': lambda i: i['read-allocation']['semantics'].update(target=[dict(id='operator', qualifiedName=i['operator']['qualifiedName'])]),
            'native-requirement-subject': lambda i: i['subject-expression']['semantics'].update(referent=dict(id='read', qualifiedName=i['read']['qualifiedName'])),
            'native-requirement-polarity': lambda i: i['criterion-membership']['semantics'].update(kind='assumption'),
            'native-verification-target': lambda i: i['review']['semantics'].update(verifiedRequirement=[]),
            'native-scenario-guard': lambda i: i['next']['semantics'].update(guardExpression=None),
            'native-scenario-function': lambda i: i['step-c']['semantics'].update(type=i['read']['semantics']['type']),
        }
        for code, mutate in mutations.items():
            with self.subTest(code=code):
                p, report, bindings, index = native_fixture(); count = len(report['elements'])
                mutate(index)
                result = check_native_bindings(p, report, bindings)
                self.assertFalse(result['passed'])
                self.assertEqual(len(report['elements']), count)
                self.assertIn(code, [x['code'] for x in result['issues']])

    def test_recipe_source_and_epistemic_metadata_are_bound(self):
        for mutation, code in [('recipe', 'native-recipe-mismatch'), ('model', 'native-source-mismatch'), ('basis', 'native-assertion-metadata')]:
            with self.subTest(mutation=mutation):
                p, report, bindings, index = native_fixture()
                if mutation == 'recipe': p['scope']['decision'] = 'A changed decision'
                elif mutation == 'model': bindings['modelSha256'] = 'b' * 64
                else: index['read-doc']['semantics']['body'] = 'Basis: source-explicit; status: accepted.'
                result = check_native_bindings(p, report, bindings)
                self.assertFalse(result['passed'])
                self.assertIn(code, [x['code'] for x in result['issues']])


if __name__ == '__main__':
    unittest.main()
