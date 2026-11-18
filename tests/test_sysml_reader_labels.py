"""Reader label wiring preserves qualified recipes and typed graph identities."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import sysml_reader as reader


def fixture():
    integrity, _, _ = reader.specialist()
    request = dict(id='journey-flow', view='action-flow',
                   readerProfile='action-flow', names=['Demo::Journey'])
    def element(identity, name, kind, **semantics):
        return dict(sessionElementId=identity, name=name, qualifiedName='Demo::Journey::' + name,
                    metaclass=kind, line=1, endLine=1, source=name, semantics=semantics)
    root = element('root', 'Journey', 'ActionDefinition')
    root['qualifiedName'] = 'Demo::Journey'
    elements = [root,
                element('receive', 'step1', 'ActionUsage', owner={'id': 'root'}),
                element('transfer', 'step2', 'ActionUsage', owner={'id': 'root'}),
                element('order', 'next', 'SuccessionAsUsage', owner={'id': 'root'},
                        sourceFeature=[{'id': 'receive'}], targetFeature=[{'id': 'transfer'}])]
    report = dict(staticChecksPassed=True, semanticFieldsVersion=2, sourceSha256='a' * 64,
                  reportIntegrity={'status': 'verified-managed', 'reportSha256': 'b' * 64},
                  elements=elements, views=[dict(id=request['id'], viewRecipeSha256=integrity.view_recipe_sha256(request))])
    return report, request


class ReaderLabelTests(unittest.TestCase):
    def test_global_labels_reach_typed_diagram_without_changing_recipe_or_relations(self):
        report, request = fixture()
        before = deepcopy((report, request))
        original = reader.project_views(report, [request], 'package Demo;', 'model.sysml')
        result = reader.project_views(report, [request], 'package Demo;', 'model.sysml',
                                      labels={'Demo::Journey::step1': 'Receive passenger',
                                              'Demo::Journey::step2': 'Validate journey'})
        view, baseline = result['views'][0], original['views'][0]
        self.assertEqual([n['label'] for n in view['nodes']], ['Receive passenger', 'Validate journey'])
        self.assertIn('Receive passenger', view['svg'])
        self.assertEqual(view['edges'], baseline['edges'])
        self.assertEqual([n['selectionKey'] for n in view['nodes']], [n['selectionKey'] for n in baseline['nodes']])
        self.assertEqual(result['evidence'], original['evidence'])
        self.assertEqual((report, request), before)

    def test_view_labels_override_global_labels_after_original_recipe_verification(self):
        report, request = fixture()
        request['labels'] = {'Demo::Journey::step1': 'Receive assisted passenger'}
        report['views'][0]['viewRecipeSha256'] = reader.specialist()[0].view_recipe_sha256(request)
        result = reader.project_views(report, [request], 'package Demo;', 'model.sysml',
                                      labels={'Demo::Journey::step1': 'Receive passenger'})
        self.assertEqual(result['views'][0]['nodes'][0]['label'], 'Receive assisted passenger')
        altered = deepcopy(request)
        altered['names'] = ['Demo::DifferentJourney']
        with self.assertRaisesRegex(ValueError, 'recipe differs'):
            reader.project_views(report, [altered], 'package Demo;', 'model.sysml', labels={})

    def test_invalid_label_map_is_not_silently_ignored(self):
        report, request = fixture()
        with self.assertRaisesRegex(ValueError, 'labels must map'):
            reader.project_views(report, [request], 'package Demo;', 'model.sysml',
                                 labels={'Demo::Journey::step1': {'text': 'Receive passenger'}})


if __name__ == '__main__':
    unittest.main()

