"""Question-based checks for the teaching study, not source entailment proof."""
import json,hashlib,argparse
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--bundle',type=Path,required=True);args=parser.parse_args()
p=Path(__file__).parent;a=json.loads((p/'architecture.json').read_text());b=json.loads((args.bundle/'bindings.json').read_text())
checks=[]
def check(question,actual):
 checks.append(dict(question=question,passed=bool(actual)))
r={x['id']:x for rows in a.values() if isinstance(rows,list) for x in rows if isinstance(x,dict) and 'id' in x}
def edge(sc,f,t,text=None):
 return any(e['from']==f and e['to']==t and (text is None or text in e['condition']) for e in r[sc]['transitions'])
check('Does package anatomy retain metadata, method, references, scripts and assets?',all(r[i].get('parent')=='LC_PACKAGE' for i in ['LC_META','LC_METHOD','LC_REF','LC_SCRIPT','LC_ASSET']))
check('Are passive package constituents kept distinct from runtime performers?',not any(x['component'] in ['LC_PACKAGE','LC_META','LC_METHOD','LC_REF','LC_SCRIPT','LC_ASSET'] for x in a['allocations']))
check('Can the agent proceed without matching a skill?',edge('SC_DISCLOSE','select','plain'))
check('Does selected instruction loading follow selection, not precede it?',edge('SC_DISCLOSE','select','load') and edge('SC_DISCLOSE','load','plan'))
check('Are extra references conditional rather than eagerly required?',edge('SC_DISCLOSE','plan','reference','needed') and edge('SC_DISCLOSE','plan','answer'))
check('Can instruction-only tasks bypass tools?',edge('SC_EXEC','plan','verify','No operation'))
check('Does a missing prerequisite preserve an unresolved outcome?',edge('SC_EXEC','gate','block') and not edge('SC_EXEC','gate','answer'))
check('Is a returned tool error distinct from a verified answer?',edge('SC_EXEC','result','block') and edge('SC_EXEC','result','verify'))
check('Does failed verification avoid a success terminal?',edge('SC_EXEC','verify','block'))
check('Does the host remain the source of permission disposition?',r['CX_2']['source']=='HOST' and r['CX_2']['target']=='LC_EXEC')
check('Do operation requests and results have opposite tool-boundary directions?',r['CX_3']['source']=='LC_EXEC' and r['CX_3']['target']=='TOOLS' and r['CX_4']['source']=='TOOLS' and r['CX_4']['target']=='LC_EXEC')
check('Are candidate and baseline outcomes both input to comparison?',r['X_11']['item']=='Candidate and baseline revisions' and r['X_12']['item']=='Observed paired results')
check('Does a changed candidate re-enter trials?',edge('SC_IMPROVE','revise','trial'))
check('Is release after comparison rather than after editing?',edge('SC_IMPROVE','compare','release') and not edge('SC_IMPROVE','draft','release'))
check('Is source interpretation before model authoring?',edge('SC_SYSML','interpret','model'))
check('Is source meaning repaired in the model?',edge('SC_SYSML','verify','model','Source-meaning'))
check('Is visual failure repaired in rendering without distorting the model?',edge('SC_SYSML','verify','render','Layout or interaction'))
check('Are qualification errors repaired rather than rendered as success?',edge('SC_SYSML','qualify','model') and edge('SC_SYSML','qualify','render','qualified'))
check('Does proposed revision lifecycle distinguish evaluation and release?',r['SM_REVISION']['basis']=='proposed' and any(t['from']=='evaluating' and t['to']=='released' for t in r['SM_REVISION']['transitions']))
check('Are planned checks not represented as executed?',all(v['status']=='planned' for v in a['verificationCases']))
check('Are source and candidate hashes bound to exact bytes?',a['source']['sha256']==hashlib.sha256((p/'source.md').read_bytes()).hexdigest() and b['modelSha256']==hashlib.sha256((args.bundle/'model.sysml').read_bytes()).hexdigest())
result=dict(passed=all(c['passed'] for c in checks),checks=checks,scope='Question-based source distinctions and graph semantics, alongside separate native qualification; not browser execution or standards certification.')
print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
