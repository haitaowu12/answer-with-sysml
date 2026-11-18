"""Model consistency and negative-case checks for the multi-view reader."""
import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import sysml_reader as reader
from sysml_reader_native import native_spec

FIXTURE = ROOT/'.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/authoring/pump-station'
SKILL = ROOT/'.agent/skills/knowledge-engine/specialists/sysml-v2-modeling'


class MappingTests(unittest.TestCase):
    def test_registry_has_one_route_per_standard_family_and_no_false_geometry_match(self):
        registry = json.loads((reader.PACKAGE/'sysml-view-map.json').read_text())
        names = [f['sysml'] for f in registry['families']]
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual(set(names), {'GeneralView','InterconnectionView','ActionFlowView','StateTransitionView',
                                     'SequenceView','GeometryView','GridView','BrowserView'})
        geo = next(f for f in registry['families'] if f['sysml']=='GeometryView')
        self.assertIsNone(geo['native']);self.assertIn('geometry',geo['implemented'])
        self.assertIn('action-flow',next(f for f in registry['families'] if f['sysml']=='ActionFlowView')['implemented'])
        self.assertIn('membership',next(f for f in registry['families'] if f['sysml']=='BrowserView')['implemented'])
        self.assertIn('decomposition',next(f for f in registry['families'] if f['sysml']=='GeneralView')['implemented'])

    def test_unresolved_endpoints_are_refused_before_drawing(self):
        p={'viewKind':'connections','scopeElementId':'scope','nodes':[{'id':'a','role':'component','label':'A'}],
           'edges':[{'source':'a','target':'missing','elementId':'e','kind':'connection','label':'Contact'}]}
        with self.assertRaisesRegex(ValueError,'unresolved'):reader.graph_facts(p)

    def test_parallel_or_unknown_state_scope_cannot_be_flattened(self):
        nodes=[{'id':'root','readerId':'r','parent':None,'parallel':False,'elementId':'root','label':'Operating'},
               {'id':'a','readerId':'a','parent':'root','parallel':False,'elementId':'a','label':'Ready'},
               {'id':'b','readerId':'b','parent':'root','parallel':False,'elementId':'b','label':'Active'}]
        edges=[{'id':'e','source':'a','target':'b','label':'Start'}]
        p={'viewKind':'states','title':'Operating','behavior':{'rootId':'root','relations':[]}}
        for parallel in (True,None):
            candidate=copy.deepcopy(nodes);candidate[0]['parallel']=parallel
            with self.assertRaisesRegex(ValueError,'concurrent'):native_spec(p,candidate,edges,{})


@unittest.skipUnless(shutil.which('java') and shutil.which('dot') and (SKILL/'.runtime/sysml').exists(),
                     'Reference SysML runtime, Java and Graphviz required')
class QualifiedReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='qualified reader test ')
        cls.root=Path(cls.temp.name);cls.source=cls.root/'model.sysml'
        cls.source.write_bytes((FIXTURE/'model.sysml').read_bytes())
        cls.recipes=cls.root/'views.json';cls.recipes.write_bytes((FIXTURE/'views.json').read_bytes())
        cls.qualified=cls.root/'qualified';cls.output=cls.root/'reader'
        result=subprocess.run([sys.executable,str(SKILL/'scripts/sysml.py'),'qualify','--source',str(cls.source),
            '--views',str(cls.recipes),'--output',str(cls.qualified)],text=True,capture_output=True,timeout=180)
        if result.returncode:raise AssertionError(result.stdout+result.stderr)
        reader.build(cls.source,cls.qualified/'report.json',cls.recipes,cls.output,title='Pump station')
        cls.data=json.loads((cls.output/'reader.json').read_text())
        cls.views={v['id']:v for v in cls.data['views']}

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_one_revision_ten_presentations_and_preserved_model(self):
        self.assertEqual(len(self.views),10)
        self.assertEqual({v['sourceSha256'] for v in self.views.values()},{reader.digest(self.source.read_bytes())})
        self.assertEqual((self.output/'model.sysml').read_bytes(),self.source.read_bytes())
        self.assertEqual({v['nativeDiagram']['diagram_type'] for v in self.views.values()},
                         {'architecture','tree','lifecycle','dataflow','custom-ports','custom-matrix'})
        for view in self.views.values():
            self.assertIn(view['standardView'],{'GeneralView','InterconnectionView','BrowserView','StateTransitionView','GridView'})
            for node in view['nodes']:self.assertIn(node['elementId'],self.data['evidence'])
            for edge in view['edges']:self.assertIn(edge['elementId'],self.data['evidence'])
            if 'svg' in view:
                svg=ET.fromstring(view['svg'])
                self.assertNotIn('archify',''.join(svg.itertext()).lower())
        self.assertIn('allow-scripts allow-downloads',(self.output/'index.html').read_text())

    def test_matrix_symmetry_and_directed_transfers_have_exact_source_witnesses(self):
        v=self.views['station-structure-matrix'];cells={(c['row'],c['column']):c['relations'] for c in v['matrix']}
        self.assertEqual(len(v['edges']),5)
        self.assertEqual(len(v['nodes']),4)
        self.assertEqual(sum(e['kind']=='flow' for e in v['edges']),2)
        for edge in v['edges']:
            self.assertIn(edge['id'],cells[edge['source'],edge['target']])
            reverse=cells.get((edge['target'],edge['source']),[])
            if edge['kind']=='flow':self.assertNotIn(edge['id'],reverse)
            else:self.assertIn(edge['id'],reverse)
        self.assertEqual(v['derivedFrom'],'station-structure')
        self.assertEqual(v['edges'],self.views[v['derivedFrom']]['edges'])

    def test_usage_overview_keeps_exact_components_without_a_phantom_boundary(self):
        view = self.views['context']
        self.assertEqual(view['projection']['viewKind'], 'connections')
        self.assertEqual(view['nativeDiagram']['diagram_type'], 'architecture')
        self.assertEqual({n['label'] for n in view['nodes']}, {'Operator', 'Station'})
        self.assertNotIn(view['projection']['scopeElementId'], {n['elementId'] for n in view['nodes']})
        self.assertEqual({n['elementId'] for n in view['nodes']},
                         {n.get('elementId', n['id']) for n in view['projection']['nodes']})
        self.assertNotIn('context-matrix', self.views)

    def test_repeated_motors_remain_distinct_and_duty_selection_matches(self):
        tree=self.views['station-decomposition'];ports=self.views['station-structure']
        motors=[n for n in tree['nodes'] if n['label'].split('\n')[0]=='Motor']
        self.assertEqual(len(motors),2)
        self.assertNotEqual(motors[0]['selectionKey'],motors[1]['selectionKey'])
        duty=next(n for n in tree['nodes'] if n['label'].split('\n')[0]=='Duty')
        counterpart=next(n for n in ports['nodes'] if n['elementId']==duty['elementId'])
        self.assertEqual(duty['selectionKey'],counterpart['selectionKey'])
        custom=ports['nativeDiagram'];self.assertEqual(len(custom['connectors']),3);self.assertEqual(len(custom['flows']),2)
        self.assertGreater(sum(n['role']=='port' for n in ports['nodes']),0)

    def test_native_lifecycle_keeps_all_transitions_without_inventing_outcome(self):
        v=self.views['motor-states'];spec=v['nativeDiagram']
        self.assertEqual(len(spec['states']),3);self.assertEqual(len(spec['transitions']),4)
        self.assertEqual({s['type'] for s in spec['states']},{'neutral'})
        self.assertEqual({t['variant'] for t in spec['transitions']},{'default'})
        self.assertNotIn('data-lifecycle-initial-marker',v['svg'])
        self.assertNotIn('initial state',''.join(ET.fromstring(v['svg']).itertext()))
        self.assertEqual(len(v['readingRows']),4)
        self.assertEqual({r['elementIds'][0] for r in v['readingRows']},{e['elementId'] for e in v['edges']})
        self.assertNotIn('entryAction',json.dumps(v['readingRows']))
        svg=ET.fromstring(self.views['context']['svg'])
        for edge in self.views['context']['edges']:
            marks=[g for g in svg.iter() if g.get('data-model-relation')==edge['elementId']]
            arrows=[g for mark in marks for g in mark.iter() if g.get('marker-end')]
            self.assertEqual(bool(arrows),edge['kind']=='flow')
            if edge['kind']!='flow':
                self.assertTrue(all(mark.get('data-edge-traversal')=='inspect' for mark in marks))

    def test_stale_source_and_recipe_revision_leave_last_good_export_intact(self):
        before={str(p.relative_to(self.output)):p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
        original=self.source.read_bytes();self.source.write_bytes(original+b'\n// changed revision\n')
        try:
            with self.assertRaises(ValueError):reader.build(self.source,self.qualified/'report.json',self.recipes,self.output,replace=True)
        finally:self.source.write_bytes(original)
        original=self.recipes.read_bytes();recipes=json.loads(original);recipes[0]['names']=['Missing::Scope']
        self.recipes.write_text(json.dumps(recipes))
        try:
            with self.assertRaisesRegex(ValueError,'recipe differs'):reader.build(self.source,self.qualified/'report.json',self.recipes,self.output,replace=True)
        finally:self.recipes.write_bytes(original)
        self.assertEqual(before,{str(p.relative_to(self.output)):p.read_bytes() for p in self.output.rglob('*') if p.is_file()})
        self.assertFalse(self.output.with_name(self.output.name+'.reader-lock').exists())


if __name__=='__main__':unittest.main()

