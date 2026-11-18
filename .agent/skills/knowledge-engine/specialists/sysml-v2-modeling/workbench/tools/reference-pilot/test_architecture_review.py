"""Source binding, projection identity and inert-content contracts for the reader."""
from copy import deepcopy
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from architecture_model import build as emit
from architecture_review import assurance, build, digest


def packet():
    def r(identity, label, **extra):
        return dict(dict(id=identity, label=label, sourceRefs=['D01, PDF 1'],
                         basis='proposed', status='proposed'), **extra)
    return dict(schemaVersion=1, title='Independent service fixture', scope=dict(name='Service review', decision='Review the handover'),
        actors=[r('A1', 'Operator')],
        operationalActivities=[r('OA0', 'Operate'), r('OA1', 'Complete the service', parent='OA0', performer='A1', participants=[])],
        functions=[r('F0', 'Deliver service'), r('G1', 'Receive and process', parent='F0'), r('G2', 'Complete', parent='F0'),
                   r('F1', 'Receive request', parent='G1', realizes=['OA1']), r('F2', 'Process request', parent='G1', realizes=['OA1']),
                   r('F3', 'Complete request', parent='G2', realizes=['OA1'])],
        exchanges=[r('X1', 'Request', source='F1', target='F2', item='Request', condition='A request exists'),
                   r('X2', 'Result', source='F2', target='F3', item='Result', condition='Processing completes')],
        logicalComponents=[r('C0', 'Service'), r('C1', 'Processing responsibility', parent='C0'), r('C2', 'Completion responsibility', parent='C0')],
        allocations=[r('AL1', 'Receive allocation', function='F1', component='C1'), r('AL2', 'Process allocation', function='F2', component='C1'), r('AL3', 'Complete allocation', function='F3', component='C2')],
        scenarios=[r('SC1', 'Ordinary request', kind='nominal', slice='SC1', entryStep='a', exitSteps=['c'],
                     entryConditions=['A request exists'], exitConditions=['Completion is recorded'],
                     steps=[dict(id='a', function='F1', label='Receive'), dict(id='b', function='F2', label='Process'), dict(id='c', function='F3', label='Complete')],
                     transitions=[dict(id='T1', **{'from':'a','to':'b'}, condition='Request accepted'), dict(id='T2', **{'from':'b','to':'c'}, condition='Result available')]),
                   r('SC2', 'Two required contributions', kind='recovery', slice='SC2', entryStep='a', exitSteps=['d'],
                     entryConditions=['Both contributions are required'], exitConditions=['Both contributions reach the join'],
                     steps=[dict(id='a', function='F1', label='Coordinate'), dict(id='b', function='F2', label='First contribution'), dict(id='c', function='F3', label='Second contribution'), dict(id='d', function='F1', label='Review both contributions')],
                     transitions=[dict(id='T3', **{'from':'a','to':'b'}, condition='Selected case', kind='parallel'), dict(id='T4', **{'from':'a','to':'c'}, condition='Selected case', kind='parallel'), dict(id='T5', **{'from':'b','to':'d'}, condition='First complete', kind='join'), dict(id='T6', **{'from':'c','to':'d'}, condition='Second complete', kind='join')],
                     parallelGroups=[dict(id='PG', **{'from':'a'}, branches=['b','c'], join='d', description='Two required concurrent contributions')])],
        requirements=[r('REQ1', 'Retain request identity', subject='F1', condition='On receipt', criterion='The same request identity remains available', verificationIds=['V1'])],
        verificationCases=[r('V1', 'Review request identity', status='planned', requirementIds=['REQ1'], method='Inspection', expectedResult='Identity remains traceable')],
        decisions=[r('DEC1', 'Agree ownership', question='Who owns completion?', affects=['F3'], options=['Responsible service', 'Delegated service'])],
        stateMachines=[r('SM1', 'Service readiness', subject='C1', initial='u', terminalStates=['r'], states=[dict(id='u',label='Unavailable'),dict(id='r',label='Ready')], transitions=[dict(id='st', **{'from':'u','to':'r'}, event='Readiness evidence received', guard='Evidence accepted', effect='Permit selected service')])],
        insights=[r('I1', 'The handover matters', observation='Two responsibilities exchange a result', implication='Agree its acceptance condition', relatedIds=['X2'])],
        contextExchanges=[r('CX1','Service request',source='A1',target='C1',item='Service request')], parameters=[],
        coverage=dict(sourceSections=[dict(sourceSection='1',label='Service',modelIds=['F0'],disposition='modelled concern',reason='Functional responsibility represented')],oldJourneyIds=[]))


class ReaderData(HTMLParser):
    def __init__(self, page):
        super().__init__(); self.in_data=False; self.raw=''; self.scripts=0; self.feed(page)
    def handle_starttag(self, tag, attrs):
        if tag=='script':
            self.scripts+=1;self.in_data=dict(attrs).get('id')=='reader-data'
    def handle_data(self, data):
        if self.in_data:self.raw+=data
    def handle_endtag(self, tag):
        if tag=='script':self.in_data=False


class ArchitectureReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.model=self.root/'model';emit(packet(),self.model)
    def tearDown(self):self.temp.cleanup()
    def render(self, name='reader', **kwargs):
        output=self.root/name
        result=build(self.model/'architecture.json',self.model/'model.sysml',self.model/'bindings.json',output,**kwargs)
        parsed=ReaderData((output/'review.html').read_text())
        return result,json.loads(parsed.raw),output,parsed

    def test_connected_views_are_distinct_and_model_input_is_preserved(self):
        before=(self.model/'model.sysml').read_bytes()
        result,data,output,parsed=self.render()
        self.assertFalse(result['nativeChecked'])
        self.assertEqual((output/'model.sysml').read_bytes(),before)
        self.assertEqual((self.model/'model.sysml').read_bytes(),before)
        flow=data['views']['functions|flow|G1'];tree=data['views']['functions|decomposition|G1']
        self.assertNotEqual(flow['question'],tree['question'])
        self.assertEqual(set(flow['relationIds']),{'X1','X2'})
        self.assertNotEqual(set(flow['relationIds']),set(tree['relationIds']))
        for view in data['views'].values():
            svg=ET.fromstring(view['svg'])
            marks=[e for e in svg.iter() if e.get('data-record-id')]
            self.assertEqual(len(marks),view['nodeCount']+view['relationCount'])
            self.assertTrue(all(e.get('data-record-id') in data['records'] for e in marks))
            self.assertTrue((output/view['file']).is_file())
        self.assertEqual(parsed.scripts,2)

    def test_parallel_group_has_separate_native_bound_fork_join_and_conditions(self):
        _,data,_,_=self.render()
        view=data['views']['scenarios|scenario|SC2']
        self.assertIn('SC2/PG/fork',view['nodes']);self.assertIn('SC2/PG/join',view['nodes'])
        self.assertEqual(data['records']['SC2/PG/fork']['native']['metaclass'],'ForkNode')
        self.assertEqual(data['records']['T3']['displaySource'],'SC2/PG/fork')
        self.assertEqual(data['records']['T5']['displayTarget'],'SC2/PG/join')
        self.assertEqual(data['records']['SC2']['entryConditions'],['Both contributions are required'])
        self.assertEqual(data['records']['T3']['condition'],'Selected case')

    def test_external_text_cannot_end_data_script_and_evidence_is_single_inventory(self):
        hostile='</script><script>window.unsafe=true</script><img src=x onerror=alert(1)>'
        value=packet();value['actors'][0]['label']=hostile
        emit(value,self.root/'hostile')
        evidence=self.root/'whole-data.json';evidence.write_text(json.dumps({'records':[dict(id='EV1',label=hostile,text=hostile,kind='Source')]}))
        output=self.root/'safe'
        build(self.root/'hostile/architecture.json',self.root/'hostile/model.sysml',self.root/'hostile/bindings.json',output,evidence=evidence)
        page=(output/'review.html').read_text();parsed=ReaderData(page);data=json.loads(parsed.raw)
        self.assertEqual(parsed.scripts,2)
        self.assertEqual(data['evidence'][0]['text'],hostile)
        self.assertEqual(len(data['evidence']),1)
        self.assertNotIn('<img src=x',page)

    def test_changed_model_recipe_or_existing_reader_is_refused(self):
        self.render()
        with self.assertRaisesRegex(ValueError,'already exist'):self.render()
        path=self.model/'model.sysml';path.write_text(path.read_text()+'\n// Changed model\n')
        with self.assertRaisesRegex(ValueError,'model bytes'):self.render('stale')
        self.assertFalse((self.root/'stale').exists())

    def test_receipt_needs_all_matching_inputs_and_successful_native_facts(self):
        a=(self.model/'architecture.json').read_bytes();m=(self.model/'model.sysml').read_bytes();b=(self.model/'bindings.json').read_bytes()
        receipt=dict(architectureSha256=digest(a),modelSha256=digest(m),bindingsSha256=digest(b),
                     nativeValidation='managed-report-and-facts-checked',native={'passed':True},structuralConsistencyPassed=True,
                     reviewReadiness='review-required',engineeringAcceptance='not-assessed')
        self.assertTrue(assurance(receipt,a,m,b)['nativeChecked'])
        self.assertEqual(assurance(receipt,a,m,b)['reviewReadiness'],'review-required')
        for field in ['architectureSha256','modelSha256','bindingsSha256']:
            stale=deepcopy(receipt);stale[field]='0'*64
            self.assertFalse(assurance(stale,a,m,b)['nativeChecked'])
        bad=deepcopy(receipt);bad['native']['passed']=False
        self.assertFalse(assurance(bad,a,m,b)['nativeChecked'])


if __name__=='__main__':unittest.main()
