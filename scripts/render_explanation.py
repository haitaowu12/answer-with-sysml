#!/usr/bin/env python3
"""Render a question-led answer from a qualified architecture and a presentation plan.

The plan chooses explanation, not semantics. Every model card resolves through the
qualified recipe/binding set. Native diagrams remain unchanged. No external assets.
"""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import re

THEMES = {
 'paper': ('#faf8f4','#242333','#585469','#6554c0','#e9e4fa','#d27d34'),
 'blueprint': ('#f1f5fc','#152544','#50617e','#285dc5','#e1eafa','#a95024'),
 'ink': ('#f6f5fa','#242033','#635d72','#763e92','#f0e4f7','#aa5828'),
}
def sha(raw): return hashlib.sha256(raw).hexdigest()
def esc(s): return html.escape(str(s), quote=True)
def encoded(raw, mime): return 'data:'+mime+';base64,'+base64.b64encode(raw).decode()
def canonical(d): return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def index_recipe(recipe):
 return {r['id']:r for rows in recipe.values() if isinstance(rows,list) for r in rows if isinstance(r,dict) and isinstance(r.get('id'),str)}

def validate(plan, recipe, bindings, model):
 if bindings.get('modelSha256') != sha(model): raise ValueError('model/bindings revision mismatch')
 if bindings.get('recipeSha256') != sha(canonical(recipe)): raise ValueError('recipe/bindings revision mismatch')
 if plan.get('modelSha256') != sha(model): raise ValueError('plan model revision mismatch')
 if plan.get('theme') not in THEMES: raise ValueError('choose an explicit supported theme')
 records=index_recipe(recipe); bound=bindings['elements']; seen=set()
 if not plan.get('sections'): raise ValueError('answer needs question sections')
 for section in plan['sections']:
  sid=section.get('id','')
  if not re.fullmatch(r'[a-z][a-z0-9-]*',sid) or sid in seen: raise ValueError('invalid or duplicate section identity')
  seen.add(sid)
  if not section.get('question') or not section.get('answer'): raise ValueError('section needs a question and answer')
  if section.get('layout') not in ('composition','process','contrast','relationships'): raise ValueError('unknown representation')
  ids=section.get('modelIds',[])
  if not ids or any(i not in records or i not in bound for i in ids): raise ValueError('unbound explanation concept')
  if len(set(ids))!=len(ids): raise ValueError('duplicate explanation concept')
  if any(not records[i].get('sourceRefs') for i in ids): raise ValueError('explanation concept lacks source grounding')
  if section['layout']=='process':
   scenario=records.get(section.get('scenarioId'),{})
   steps={step['id']:step['function'] for step in scenario.get('steps',[])}
   relations={(steps.get(t['from']),steps.get(t['to'])) for t in scenario.get('transitions',[])}
   if any((a,b) not in relations for a,b in zip(ids,ids[1:])) or len(ids)<2: raise ValueError('process order must follow explicit scenario transitions')
   if not section.get('diagram'): raise ValueError('selected process path requires its full native scenario')
 return records

CSS='''
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:100px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 system-ui,-apple-system,sans-serif}a{color:var(--accent)}a:focus-visible,summary:focus-visible{outline:3px solid var(--secondary);outline-offset:5px}main{max-width:1200px;margin:auto;padding:50px 40px 80px}header{padding:25px 0 44px;border-bottom:1px solid var(--line)}h1{font-size:clamp(42px,6.5vw,84px);letter-spacing:-.065em;line-height:1.02;font-weight:750;max-width:900px;margin:0 0 28px}.lede{font-size:clamp(20px,2.3vw,27px);max-width:780px;color:var(--muted);margin:0}nav{position:sticky;top:0;z-index:2;padding:17px 0;background:var(--bg);display:flex;gap:8px;overflow:auto;border-bottom:1px solid var(--line)}nav a{white-space:nowrap;text-decoration:none;font-size:14px;font-weight:650;padding:9px 14px;border:1px solid var(--line);border-radius:30px;color:var(--ink)}nav a:hover,nav a[aria-current]{background:var(--ink);color:var(--bg)}section{padding:55px 0;border-bottom:1px solid var(--line);scroll-margin-top:15px}.section-head{display:grid;grid-template-columns:70px 1fr;gap:18px;margin-bottom:28px}.number{color:var(--secondary);font:600 36px/1.2 ui-monospace,monospace}h2{font-size:clamp(27px,3.4vw,42px);letter-spacing:-.035em;line-height:1.12;margin:0 0 15px}.answer{max-width:800px;color:var(--muted);font-size:19px;margin:0}.visual{display:grid;gap:14px}.composition{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.concept{border:1px solid var(--line);background:white;padding:24px;min-width:0;border-radius:4px}.concept h3{margin:0 0 12px;font-size:21px;letter-spacing:-.025em}.concept p{color:var(--muted);margin:0;font-size:15px}.concept code{font-size:11px;color:var(--muted)}.composition .concept:first-child{background:var(--tint);border-top:4px solid var(--accent)}.condition{margin-top:16px!important;padding:10px 12px;background:var(--tint);border-left:2px solid var(--accent);font-size:13px!important;color:var(--ink)!important}.condition span{display:block;font:650 10px/1.4 ui-monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}.path-label{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}.process{grid-template-columns:1fr;counter-reset:steps}.process .concept{position:relative;counter-increment:steps;margin-left:45px;border-left:3px solid var(--accent);padding:22px 25px}.process .concept:before{content:counter(steps);position:absolute;left:-46px;top:22px;color:var(--accent);font:700 20px/1.3 ui-monospace}.process .concept:not(:last-child):after{content:'↓';position:absolute;left:-41px;bottom:-24px;color:var(--muted)}.contrast{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.contrast .concept{border-top:5px solid var(--accent)}.contrast .concept:nth-child(even){border-top-color:var(--secondary);background:#fff9f2}.relationships{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}.relationships .concept{border-left:4px solid var(--secondary)}.relationships .endpoints{display:flex;align-items:center;gap:10px;margin:10px 0;font-size:16px;font-weight:650}.flow-arrow{color:var(--secondary)}details{margin-top:15px;border-top:1px solid var(--line);font-size:13px}summary{padding:12px 0;cursor:pointer;font-weight:650}details p{font-size:13px!important;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.55 ui-monospace,monospace}.diagram{margin:28px 0 0;border:1px solid var(--line);padding:20px;background:white;overflow:auto}.diagram img{display:block;width:100%;min-width:640px;height:auto}.diagram figcaption{font-size:13px;color:var(--muted);margin-top:15px}.downloads{display:flex;flex-wrap:wrap;gap:12px;margin-top:35px}.downloads a{padding:11px 18px;border:1px solid var(--line);border-radius:5px;font-size:14px;text-decoration:none}.trace{display:grid;grid-template-columns:1fr 25px 1fr 25px 1fr;align-items:center;gap:12px;margin-top:28px;padding:25px;background:var(--ink);color:var(--bg);border-radius:6px}.trace>div{min-width:0}.trace-label{display:block;font:650 11px/1.3 ui-monospace;letter-spacing:.08em;text-transform:uppercase;color:#d5c9ee}.trace p,.trace pre{font-size:14px}.trace small{font-size:10px;overflow-wrap:anywhere;color:#d5c9ee}.trace h3{font-size:23px;margin:14px 0}.trace-arrow{font-size:26px;color:#eab26f}.sources{font-size:14px}.sources p{margin:12px 0}.source-role{color:var(--muted)}footer{margin-top:20px;font-size:12px;color:var(--muted)}@media(max-width:650px){.trace{grid-template-columns:1fr;padding:22px}.trace-arrow{transform:rotate(90deg);justify-self:center}main{padding:25px 20px 50px}header{padding:20px 0 30px}section{padding:35px 0}.section-head{grid-template-columns:35px 1fr;gap:10px}.number{font-size:22px}.concept{padding:19px}.composition,.contrast,.relationships{grid-template-columns:1fr}nav{padding:12px 0}nav a{font-size:12px;padding:8px 11px}.answer{font-size:17px}.diagram{padding:10px}.diagram img{min-width:580px}h1{font-size:48px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}@media print{nav{position:static;flex-wrap:wrap}.downloads{display:none}section{break-before:auto}.concept{break-inside:avoid}details{display:block}main{padding:0}.diagram img{min-width:0}}
'''

def render(plan, bundle, output, source=None):
 if output.resolve().is_relative_to(bundle.resolve()): raise ValueError('answer output must be outside the qualified bundle')
 recipe=json.loads((bundle/'architecture.json').read_text());bindings=json.loads((bundle/'bindings.json').read_text());model=(bundle/'model.sysml').read_bytes()
 records=validate(plan,recipe,bindings,model)
 source_text=source.read_text() if source else ''
 if source and sha(source.read_bytes()) != recipe.get('source',{}).get('sha256'): raise ValueError('source/recipe revision mismatch')
 from sysml_reader import specialist
 integrity, _, _ = specialist()
 qualified=integrity.load_report(bundle/'qualification/report.json', source=model)
 if not qualified.get('staticChecksPassed'): raise ValueError('native qualification failed')
 native_names={e.get('qualifiedName') for e in qualified['elements']}
 if any(bindings['elements'][i]['qualifiedName'] not in native_names for section in plan['sections'] for i in section['modelIds']): raise ValueError('binding absent from qualified native model')
 result=json.loads((bundle/'build-result.json').read_text())
 if any(result.get('stages',{}).get(s)!='passed' for s in ('nativeLanguage','nativeReconciliation','readerGeneration')): raise ValueError('qualified build required')
 palette=THEMES[plan['theme']]
 variables=':root{'+''.join('--'+k+':'+v+';' for k,v in zip(('bg','ink','muted','accent','tint','secondary'),palette))+'--line:#d9d5df;}'
 nav=''.join('<a href="#'+s['id']+'">'+esc(s.get('nav',s['question']))+'</a>' for s in plan['sections'])
 sections=[]
 for n,s in enumerate(plan['sections'],1):
  cards=[]
  guards={}
  if s['layout']=='process':
   scenario=records[s['scenarioId']];steps={step['id']:step['function'] for step in scenario['steps']}
   for first,last in zip(s['modelIds'],s['modelIds'][1:]):
    matches=[t for t in scenario['transitions'] if steps.get(t['from'])==first and steps.get(t['to'])==last]
    if len(matches)!=1: raise ValueError('process path has ambiguous occurrences; use the native behavior view')
    guards[first]=matches[0].get('condition') or 'Unconditional transition'
  for i in s['modelIds']:
   r=records[i]; b=bindings['elements'][i]
   endpoints=''
   if r.get('source') in records and r.get('target') in records:
    endpoints='<div class="endpoints"><span>'+esc(records[r['source']]['label'])+'</span><span class="flow-arrow" aria-label="to">→</span><span>'+esc(records[r['target']]['label'])+'</span></div>'
   guard='<p class="condition"><span>Continue when</span>'+esc(guards[i])+'</p>' if i in guards else ''
   cards.append('<article class="concept" data-model-id="'+esc(i)+'"><h3>'+esc(r.get('label',i))+'</h3>'+endpoints+'<p>'+esc(r.get('description',''))+'</p>'+guard+'<details><summary>Model &amp; evidence</summary><p>'+esc(b['metaclass'])+' · '+esc(b['qualifiedName'])+'</p><p>'+esc(' · '.join(r.get('sourceRefs',[])))+'</p><p>'+esc(r.get('basis',''))+'</p></details></article>')
  trace=''
  if s.get('trace'):
   t=s['trace'];identity=t.get('modelId');record=records.get(identity,{})
   if identity not in s['modelIds'] or t.get('sourceRef') not in record.get('sourceRefs',[]): raise ValueError('trace is not bound to this section evidence')
   if not t.get('sourceText') or t['sourceText'] not in source_text: raise ValueError('trace text not present in exact source')
   name=bindings['elements'][identity]['qualifiedName']
   element=next(e for e in qualified['elements'] if e.get('qualifiedName')==name)
   line=element.get('line')
   if not isinstance(line,int) or line<1: raise ValueError('native trace source location unavailable')
   fragment=model.decode().splitlines()[line-1].strip()
   trace='<div class="trace"><div><span class="trace-label">Source evidence</span><p>'+esc(t['sourceText'])+'</p><small>'+esc(t['sourceRef'])+'</small></div><span class="trace-arrow" aria-label="represented by">→</span><div><span class="trace-label">Native model</span><pre>'+esc(fragment)+'</pre><small>'+esc(name)+'</small></div><span class="trace-arrow" aria-label="explained as">→</span><div><span class="trace-label">Reader view</span><h3>'+esc(record['label'])+'</h3><p>'+esc(record.get('description',''))+'</p></div></div>'
  diagram=''

  if s.get('diagram'):
   path=(bundle/'diagrams'/s['diagram']).resolve()
   if path.parent!=(bundle/'diagrams').resolve() or path.suffix!='.svg': raise ValueError('diagram must be a local generated SVG')
   diagram='<figure class="diagram"><img alt="'+esc(s.get('diagramAlt',s['question']))+'" src="'+encoded(path.read_bytes(),'image/svg+xml')+'"><figcaption>'+esc(s.get('diagramCaption',''))+'</figcaption></figure>'
   if s['layout']=='process': diagram='<details class="full-flow"><summary>Branches and recovery</summary>'+diagram+'</details>'
  path_label='<p class="path-label">Selected path</p>' if s['layout']=='process' else ''
  sections.append('<section id="'+s['id']+'"><div class="section-head"><span class="number">'+f'{n:02d}'+'</span><div><h2>'+esc(s['question'])+'</h2><p class="answer">'+esc(s['answer'])+'</p></div></div>'+path_label+'<div class="visual '+s['layout']+'">'+''.join(cards)+'</div>'+trace+diagram+'</section>')
 sources=''.join('<p><a href="'+esc(x['url'])+'">'+esc(x['title'])+'</a><br><span class="source-role">'+esc(x['role'])+'</span></p>' for x in plan.get('sources',[]) if x['url'].startswith('https://'))
 downloads=''.join('<a download="'+name+'" href="'+encoded(raw,mime)+'">'+label+'</a>' for name,raw,mime,label in [('model.sysml',model,'text/plain','SysML model'),('architecture.json',json.dumps(recipe,indent=2).encode(),'application/json','Model recipe')])
 if source: downloads+='<a download="source.md" href="'+encoded(source.read_bytes(),'text/plain')+'">Source evidence</a>'
 # Links and every section work without this optional active-section enhancement.
 js="""const links=Array.from(document.querySelectorAll('nav a'));function mark(){links.forEach(a=>{if(a.hash===location.hash)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}addEventListener('hashchange',mark);mark();"""
 page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(plan['title'])+'</title><style>'+variables+CSS+'</style></head><body><main><header><h1>'+esc(plan['title'])+'</h1><p class="lede">'+esc(plan['summary'])+'</p></header><nav aria-label="Questions">'+nav+'</nav>'+''.join(sections)+'<div class="downloads">'+downloads+'</div><details class="sources"><summary>Sources and scope</summary>'+sources+'<p>'+esc(plan.get('scope',''))+'</p></details><footer>Model revision '+sha(model)[:12]+'</footer></main><script>'+js+'</script></body></html>'
 output.write_text(page)
 return {'output':str(output),'sha256':sha(page.encode()),'modelSha256':sha(model),'sections':len(sections),'browserAcceptance':'not-run'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source',type=Path);a=p.parse_args()
 try: print(json.dumps(render(json.loads(a.plan.read_text()),a.bundle,a.output,a.source),indent=2))
 except (ValueError,KeyError,OSError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
