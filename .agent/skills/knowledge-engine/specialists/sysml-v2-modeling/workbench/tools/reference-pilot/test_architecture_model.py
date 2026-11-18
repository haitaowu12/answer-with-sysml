"""Regression cases for demonstrated native-authoring meaning/evidence losses.

These cases exercise the emitted artifact and retained failure packet. They do
not treat generated expectations, native syntax, or test success as an operating
acceptance result. The finite-state completion syntax has a separate pinned
Pilot qualification; this test checks that the adapter actually emits it.
"""
import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from architecture_check import check_architecture
from architecture_model import Emitter
from architecture_workbench import run
from test_architecture import recipe, record


def concurrent_case(alternative_completion=False):
    packet = recipe()
    scenario = packet['scenarios'][0]
    scenario['steps'] += [dict(id='b1', function='read'), dict(id='b2', function='choose')]
    scenario['parallelGroups'] = [dict(id='required-pair', **{'from': 'r'},
                                      branches=['b1', 'b2'], join='c')]
    scenario['transitions'] = [
        dict(id='branch-one', **{'from': 'r', 'to': 'b1'}, kind='parallel', condition='First required contribution is ready'),
        dict(id='branch-two', **{'from': 'r', 'to': 'b2'}, kind='parallel', condition='Second required contribution is ready'),
        dict(id='complete-one', **{'from': 'b1', 'to': 'c'}, kind='join', condition='First contribution completes'),
    ]
    if not alternative_completion:
        scenario['transitions'].append(dict(id='complete-two', **{'from': 'b2', 'to': 'c'},
                                            kind='join', condition='Second contribution completes'))
        return packet
    scenario['steps'] += [dict(id='b2a', function='choose'), dict(id='b2b', function='choose')]
    scenario['transitions'] += [
        dict(id='choose-a', **{'from': 'b2', 'to': 'b2a'}, condition='Alternative A is selected and B is not selected'),
        dict(id='choose-b', **{'from': 'b2', 'to': 'b2b'}, condition='Alternative B is selected and A is not selected'),
        dict(id='complete-a', **{'from': 'b2a', 'to': 'c'}, kind='join', condition='Alternative A completes'),
        dict(id='complete-b', **{'from': 'b2b', 'to': 'c'}, kind='join', condition='Alternative B completes'),
    ]
    return packet


def finite_state_case():
    packet = recipe()
    packet['stateMachines'] = [record('handling-state', subject='service', initial='pending',
        states=[dict(id='pending', label='Pending decision'), dict(id='complete', label='Agreed completion')],
        terminalStates=['complete'], transitions=[dict(id='finish-decision', **{'from': 'pending', 'to': 'complete'},
            event='Decision evidence arrives', guard='The agreed decision is complete', effect='Retain the decision evidence')])]
    return packet


class NativeAuthoringRegressionTests(unittest.TestCase):
    def test_alternative_branch_ends_cannot_become_additional_required_join_contributions(self):
        # A normal two-contribution case stays supported. The conditional branch
        # needs a merge, which this bounded recipe profile does not yet express.
        Emitter(concurrent_case()).emit()
        with self.assertRaises(ValueError):
            Emitter(concurrent_case(alternative_completion=True)).emit()

    def test_scenario_labels_are_native_names_and_keep_recipe_identity(self):
        packet = recipe()
        scenario = packet['scenarios'][0]
        first, second = scenario['steps']
        first['label'] = second['label'] = "Check passenger's acceptance"
        transition = scenario['transitions'][0]
        transition['condition'] = "Acceptance isn't present"
        source, bindings = Emitter(packet).emit()
        first_name = "'Check passenger\\'s acceptance'"
        second_name = f"'Check passenger\\'s acceptance ({second['id']})'"
        guard = "'Acceptance isn\\'t present'"
        parent = bindings['elements'][scenario['id']]['qualifiedName']
        self.assertEqual(bindings['elements'][f"{scenario['id']}/{first['id']}"]['qualifiedName'],
                         f'{parent}::{first_name}')
        self.assertIn(f"first {first_name} if {guard} then {second_name}", source)
        self.assertIn(f'attribute {guard} : Boolean {{', source)
        self.assertIn(f"expose {parent.rsplit('::', 1)[1]}::*;", source)
        self.assertIn('view ActionFlow : StandardViewDefinitions::ActionFlowView', source)

    def test_acceptance_claim_keeps_its_evidence_and_configuration(self):
        packet = recipe()
        component = packet['logicalComponents'][0]
        component['status'] = 'accepted'
        component['acceptanceEvidence'] = dict(record='SIGNOFF-REGRESSION-481',
                                              configuration='CONFIG-APPROVED-27')
        original = copy.deepcopy(packet)
        self.assertTrue(check_architecture(packet)['structuralConsistencyPassed'])
        source, _ = Emitter(packet).emit()
        self.assertIn('SIGNOFF-REGRESSION-481', source)
        self.assertIn('CONFIG-APPROVED-27', source)
        self.assertEqual(packet, original)

    def test_finite_and_ongoing_state_lifecycles_have_distinct_retained_semantics(self):
        finite = finite_state_case()
        finite_source, finite_bindings = Emitter(finite).emit()
        binding = finite_bindings['elements']['handling-state']
        completion = binding['terminalTransitions']['complete']
        state = binding['states']['complete']
        # Check the actual semantic relation in the native artifact, using bound
        # identities rather than fixed generated names or display wording.
        relation = (r'\btransition\s+' + re.escape(completion.rsplit('::', 1)[-1])
                    + r'\s+first\s+' + re.escape(state.rsplit('::', 1)[-1])
                    + r'\s+then\s+done\s*;')
        self.assertRegex(finite_source, relation)
        ongoing = copy.deepcopy(finite)
        machine = ongoing['stateMachines'][0]
        machine.update(terminalStates=[], terminalPolicy='ongoing',
                       lifecycleExitCondition='SERVICE-WITHDRAWAL-REGRESSION-481 ends this service lifetime.')
        ongoing_source, ongoing_bindings = Emitter(ongoing).emit()
        self.assertIn('SERVICE-WITHDRAWAL-REGRESSION-481', ongoing_source)
        self.assertEqual(ongoing_bindings['elements']['handling-state']['terminalTransitions'], {})
        self.assertNotRegex(ongoing_source, relation)
        self.assertNotEqual(ongoing_source, finite_source)

    def test_keyword_function_identity_is_preserved_without_becoming_a_keyword_declaration(self):
        packet = recipe()
        function = packet['functions'][0]
        function['id'] = 'accept'
        packet['exchanges'][0]['source'] = 'accept'
        packet['allocations'][0]['function'] = 'accept'
        packet['scenarios'][0]['steps'][0]['function'] = 'accept'
        source, bindings = Emitter(packet).emit()
        escaped = bindings['elements']['accept']['qualifiedName'].rsplit('::', 1)[-1]
        self.assertNotEqual(escaped, 'accept')
        self.assertRegex(source, r'\baction\s+' + re.escape(escaped) + r'\s*:')
        self.assertEqual(bindings['elements']['sample']['sourceId'], 'accept')
        # A second author-supplied ID with the escaped spelling must not silently
        # alias the first record or replace its native identity.
        duplicate = copy.deepcopy(packet['functions'][0]); duplicate['id'] = escaped
        packet['functions'].append(duplicate)
        with self.assertRaises(ValueError):
            Emitter(packet).emit()


class FailedAuthoringEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.input = self.root/'input.json'
        self.output = self.root/'candidate'

    def write_input(self, packet):
        # Preserve these exact bytes, not merely reserialized equivalent data.
        raw = ('\n' + json.dumps(packet, indent=3) + '\n').encode()
        self.input.write_bytes(raw)
        return raw

    def assert_failure_receipt(self, result, code, stage, raw):
        self.assertNotEqual(code, 0)
        retained = json.loads((self.output/'build-result.json').read_text())
        self.assertEqual(retained, result)
        self.assertEqual(retained['stages'][stage], 'failed')
        self.assertNotEqual(retained['status'], 'candidate-for-engineering-review')
        self.assertEqual((self.output/'input.snapshot.json').read_bytes(), raw)
        self.assertEqual(self.input.read_bytes(), raw)
        self.assertEqual(retained['verificationExecution'], 'not-run')
        self.assertEqual(retained['engineeringAcceptance'], 'not-assessed')

    def test_multi_subject_rejection_retains_failure_and_prevents_overwrite(self):
        packet = recipe()
        packet['requirements'].append(record('read-obligation', subject='read', condition='For each sample',
            criterion='A sample identity is retained.', rationale='Preserve the source identity.',
            derivedFrom=['handle'], verificationIds=['review']))
        packet['verificationCases'][0]['requirementIds'].append('read-obligation')
        self.assertTrue(check_architecture(packet)['structuralConsistencyPassed'])
        raw = self.write_input(packet)
        result, code = run(self.input, self.output, qualify=False, reader=False)
        self.assert_failure_receipt(result, code, 'nativeAuthoring', raw)
        self.assertFalse((self.output/'model.sysml').exists())
        for stage in ('nativeLanguage', 'nativeReconciliation', 'readerGeneration', 'readerInteraction'):
            self.assertNotEqual(result['stages'].get(stage), 'passed')
        before = {str(p.relative_to(self.output)):p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
        with self.assertRaises(ValueError):
            run(self.input, self.output, qualify=False, reader=False)
        after = {str(p.relative_to(self.output)):p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_reader_failure_retains_model_and_does_not_claim_unrun_checks(self):
        raw = self.write_input(recipe())
        with patch('architecture_review.build', side_effect=ValueError('Synthetic renderer rejection')):
            result, code = run(self.input, self.output, qualify=False, reader=True)
        self.assert_failure_receipt(result, code, 'readerGeneration', raw)
        self.assertTrue((self.output/'model.sysml').exists())
        self.assertEqual(result['stages']['nativeLanguage'], 'not-run')
        self.assertEqual(result['stages']['nativeReconciliation'], 'not-run')
        self.assertNotEqual(result['stages'].get('readerInteraction'), 'passed')


if __name__ == '__main__':
    unittest.main()
