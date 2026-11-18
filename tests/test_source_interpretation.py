"""Source-review expectations catch observed interpretation regressions, not prose entailment."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from review_source_interpretation import digest, review
FIXTURE = ROOT/'tests/fixtures/source-review'

class SourceInterpretationTests(unittest.TestCase):
    def setUp(self):
        self.source=(FIXTURE/'source.md').read_bytes()
        self.raw=(FIXTURE/'recipe.json').read_bytes()
        self.recipe=json.loads(self.raw)
        self.receipt=json.loads((FIXTURE/'review.json').read_text())

    def check_candidate(self, candidate):
        raw=json.dumps(candidate).encode()
        receipt=copy.deepcopy(self.receipt)
        receipt['recipeSha256']=digest(raw)
        return review(self.source,raw,receipt)

    def test_reviewed_excerpts_pass(self):
        self.assertTrue(review(self.source,self.raw,self.receipt)['passed'])

    def test_available_only_join_cannot_hide_unavailable_outcomes(self):
        self.recipe['scenarios'][0]['transitions'][0]['condition']='Validity contribution available'
        result=self.check_candidate(self.recipe)
        self.assertFalse(result['passed']);self.assertTrue(any('JOIN:' in e for e in result['errors']))

    def test_acknowledgment_label_only_repair_cannot_hide_exception_target(self):
        self.recipe['scenarios'][1]['steps'][0]['function']='F_EXCEPTION'
        result=self.check_candidate(self.recipe)
        self.assertFalse(result['passed']);self.assertTrue(any('ACK:' in e for e in result['errors']))

    def test_ack_does_not_assert_assessment_still_outstanding(self):
        self.recipe['functions'][0]['label']='Retain unresolved assessment disposition'
        self.assertFalse(self.check_candidate(self.recipe)['passed'])

    def test_each_required_boundary_message_must_be_present(self):
        for i in range(5):
            candidate=copy.deepcopy(self.recipe)
            del candidate['contextExchanges'][i]
            with self.subTest(missing=i):self.assertFalse(self.check_candidate(candidate)['passed'])

    def test_duplicate_boundary_id_is_not_coverage(self):
        self.recipe['contextExchanges'].append(copy.deepcopy(self.recipe['contextExchanges'][0]))
        self.assertFalse(self.check_candidate(self.recipe)['passed'])

    def test_source_or_recipe_change_invalidates_receipt(self):
        self.assertFalse(review(self.source+b'\nRevision',self.raw,self.receipt)['passed'])
        self.assertFalse(review(self.source,self.raw+b' ',self.receipt)['passed'])

    def test_missing_focus_pending_verdict_and_unlocated_evidence_fail(self):
        variants=[]
        r=copy.deepcopy(self.receipt);r['checks'].pop();variants.append(r)
        r=copy.deepcopy(self.receipt);r['checks'][0]['status']='pending';variants.append(r)
        r=copy.deepcopy(self.receipt);r['checks'][0]['sourceRefs']=['UNKNOWN-CLAUSE'];variants.append(r)
        r=copy.deepcopy(self.receipt);r['checks'][-1]['rationale']='';variants.append(r)
        for r in variants:self.assertFalse(review(self.source,self.raw,r)['passed'])

    def test_boolean_is_not_numeric_equality_even_when_nested(self):
        for actual, expected in [(True,1), ({'limit':True},{'limit':1}), ([True],[1])]:
            candidate=copy.deepcopy(self.recipe);candidate['limit']=actual
            raw=json.dumps(candidate).encode()
            receipt=copy.deepcopy(self.receipt);receipt['recipeSha256']=digest(raw)
            receipt['checks'][0]['assertions']=[{'path':'/limit','equals':expected}]
            with self.subTest(actual=actual):self.assertFalse(review(self.source,raw,receipt)['passed'])
        receipt=copy.deepcopy(self.receipt);receipt['schemaVersion']=True
        self.assertFalse(review(self.source,self.raw,receipt)['passed'])

    def test_missing_pointer_and_unknown_operator_fail_closed(self):
        for assertion in [{'path':'/missing','equals':True},{'path':'/functions','magic':True}]:
            r=copy.deepcopy(self.receipt);r['checks'][0]['assertions']=[assertion]
            self.assertFalse(review(self.source,self.raw,r)['passed'])

if __name__ == '__main__':unittest.main()
