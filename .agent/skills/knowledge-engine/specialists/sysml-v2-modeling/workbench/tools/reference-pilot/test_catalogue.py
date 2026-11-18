"""Regression contracts for repeated global indexes versus distinct views."""
from copy import deepcopy
import unittest

from catalogue import canonicalize, semantic_signature


def inventory(identity='whole:model-catalogue:1', scope='Whole source'):
    return dict(id=identity, label='Model catalogue · 1–2', family='model-catalogue',
                scope=scope, readerScope=scope, sourceSha256='a' * 64, reviewRevision='b' * 64,
                question='Which declarations are in the source model?',
                nodes=[dict(id='a', elementId='a', label='Receive bag'),
                       dict(id='b', elementId='b', label='Transfer bag')], edges=[],
                catalogueRows=[dict(elementId='a', sourceText='action a;'),
                               dict(elementId='b', sourceText='action b;')],
                readingRows=[], readingNote='Global source inventory',
                projection=dict(id=identity, scopeElementId=scope,
                                nodes=['a', 'b'], edges=[], warnings=[]))


class CatalogueTests(unittest.TestCase):
    def test_exact_global_content_is_single_canonical_view_with_scope_alias(self):
        source = [inventory(), inventory('context:model-catalogue:1', 'Operational context')]
        before = deepcopy(source)
        result = canonicalize(source)
        self.assertEqual(result['summary'], dict(inputViews=2, canonicalViews=1, duplicateViews=1))
        self.assertEqual(result['views'][0], source[0])
        self.assertEqual(result['aliases'][0]['id'], source[1]['id'])
        self.assertEqual(result['aliases'][0]['canonicalId'], source[0]['id'])
        self.assertEqual(result['aliases'][0]['scope'], 'Operational context')
        self.assertEqual(source, before)
        result['views'][0]['nodes'][0]['label'] = 'Changed output'
        self.assertEqual(source, before)

    def test_same_elements_with_distinct_question_or_relationship_are_not_duplicates(self):
        for field, value in (
                ('question', 'Which actors are responsible for these activities?'),
                ('edges', [dict(id='link', source='a', target='b', kind='flow')]),
                ('readingRows', [dict(title='Unresolved handover', body='Allocation is unknown')]),
                ('sourceSha256', 'c' * 64),
                ('reviewRevision', 'd' * 64),
                ('futureSemanticField', {'allocationState': 'unresolved'})):
            with self.subTest(field=field):
                other = inventory('other', 'Context')
                other[field] = value
                self.assertEqual(len(canonicalize([inventory(), other])['views']), 2)

    def test_scoped_architecture_and_local_catalogues_are_preserved(self):
        for family, catalogue_scope in (('action-flow', None), ('allocation', None),
                                        ('model-catalogue', 'local')):
            a, b = inventory(), inventory('other', 'Context')
            a['family'] = b['family'] = family
            if catalogue_scope:
                a['catalogueScope'] = b['catalogueScope'] = catalogue_scope
            self.assertEqual(len(canonicalize([a, b])['views']), 2)

    def test_missing_payload_cannot_be_declared_equivalent(self):
        for missing in ('question', 'sourceSha256', 'nodes', 'edges', 'catalogueRows'):
            a = inventory()
            a.pop(missing)
            self.assertIsNone(semantic_signature(a))
        a = inventory()
        a['sourceSha256'] = 'unknown'
        self.assertIsNone(semantic_signature(a))

    def test_invalid_identity_is_rejected_and_canonicalization_is_stable(self):
        with self.assertRaises(ValueError):
            canonicalize([inventory(), inventory()])
        result = canonicalize([inventory(), inventory('alias', 'Context')])
        again = canonicalize(result['views'])
        self.assertEqual(again['views'], result['views'])
        self.assertEqual(again['aliases'], [])


if __name__ == '__main__':
    unittest.main()
