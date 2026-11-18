"""Bounded GSN v3 core visualization, sharing the adopted interactive reader.

Consumes the retained assurance_case JSON contract. Does not mutate upstream
assurance records or infer evidence acceptance from argument connectivity.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tempfile
import textwrap
import xml.etree.ElementTree as ET

PACKAGE=Path(__file__).resolve().parents[1]/'resources/tools/archify'
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
TYPES={'goal','strategy','solution','context','assumption','justification','undeveloped_goal'}
SUPPORT={('goal','goal'),('goal','strategy'),('goal','solution'),('strategy','goal')}
CONTEXT={(a,b) for a in ('goal','strategy') for b in ('context','assumption','justification')}


def base_type(node):return 'goal' if node['type']=='undeveloped_goal' else node['type']


def validate(model):
    if not isinstance(model,dict) or not isinstance(model.get('profile'),str) or not model['profile'].startswith('gsn-v3'):
        raise ValueError('Select an explicitly GSN v3 core-profile case; legacy edges need deliberate review')
    nodes=model.get('nodes');edges=model.get('edges')
    if not isinstance(nodes,list) or not nodes or len(nodes)>200 or not isinstance(edges,list) or len(edges)>600:
        raise ValueError('Choose a bounded case with 1–200 nodes and at most 600 relationships')
    ix={}
    for n in nodes:
        if not isinstance(n,dict) or any(not isinstance(n.get(k),str) or not n[k].strip() for k in ('id','type','title','statement')):
            raise ValueError('Every GSN element needs a nonempty identity, type, title and statement')
        if n['type'] not in TYPES:raise ValueError('This GSN extension needs a separate profile: '+n['type'])
        if n['id'] in ix:raise ValueError('Duplicate GSN identity: '+n['id'])
        if 'status' in n and not isinstance(n['status'],str):raise ValueError('GSN status must be declared text')
        if 'evidence' in n and (not isinstance(n['evidence'],dict) or any(not isinstance(v,str) for v in n['evidence'].values())):raise ValueError('Evidence references must contain text fields')
        if len(n['statement'])>10000 or len(n['title'])>120 or len(n['id'])>80:raise ValueError('GSN text exceeds this reader profile')
        ix[n['id']]=n
    ids=set(ix);seen=set();pairs=set();pending={n:set() for n in ix}
    for edge in edges:
        if not isinstance(edge,dict) or any(not isinstance(edge.get(k),str) or not edge[k] for k in ('id','source','target','type')):
            raise ValueError('Every GSN relationship needs identity, source, target and type')
        if edge['id'] in seen or edge['id'] in ids:raise ValueError('Duplicate GSN relationship identity')
        seen.add(edge['id']);a=edge['source'];b=edge['target']
        if a not in ix or b not in ix:raise ValueError('Unresolved GSN relationship endpoint')
        key=(a,b,edge['type'])
        if key in pairs:raise ValueError('Duplicate GSN relationship')
        pairs.add(key)
        permitted=SUPPORT if edge['type']=='supported_by' else CONTEXT if edge['type']=='in_context_of' else set()
        if (base_type(ix[a]),base_type(ix[b])) not in permitted:raise ValueError('Relationship is not permitted in GSN v3 core: '+edge['type'])
        pending[b].add(a)
    remaining=set(ids)
    while remaining:
        ready={n for n in remaining if not pending[n]&remaining}
        if not ready:raise ValueError('GSN argument must be acyclic, including shared branches')
        remaining-=ready
    return ix


def add(parent,tag,attrs=None,content=None):
    e=ET.SubElement(parent,'{'+NS+'}'+tag,{k:str(v) for k,v in (attrs or {}).items()});e.text=content;return e


def lines(value,width):return sum([textwrap.wrap(line,width=width,break_long_words=True) or [''] for line in value.split('\n')],[])


def label(parent,x,y,value,*,width=25,size=15,weight=500):
    t=add(parent,'text',{'x':x,'y':y,'text-anchor':'middle','fill':'var(--text)','font-family':'Inter,system-ui,sans-serif','font-size':size,'font-weight':weight})
    for i,line in enumerate(lines(value,width)):add(t,'tspan',{'x':x,'dy':0 if i==0 else size*1.35},line)


def diagram(model):
    ix=validate(model);keys={key:'n'+str(i) for i,key in enumerate(ix)}
    dot=['digraph G {graph[rankdir=TB,nodesep=.55,ranksep=.85,pad=.4,splines=polyline];node[fixedsize=true,label=""];']
    sizes={}
    for key,n in ix.items():
        t=n['type'];width=3.15;height=max(1.15,(55+len(lines(n['title'],26))*21)/72)
        if t=='solution':width=height=2.1
        elif t in ('assumption','justification'):height=max(1.4,height)
        sizes[key]=(width*72,height*72)
        dot.append(f'{keys[key]}[shape={"circle" if t=="solution" else "ellipse" if t in ("assumption","justification") else "box"},width={width},height={height}];')
    for i,e in enumerate(model['edges']):
        context=e['type']=='in_context_of'
        dot.append(keys[e['source']]+'->'+keys[e['target']]+f'[id="r{i}",arrowhead=none'+(',constraint=false' if context else '')+'];')
        if context:dot.append('{rank=same;'+keys[e['source']]+';'+keys[e['target']]+';}')
    dot.append('}')
    run=subprocess.run(['dot','-Tjson'],input='\n'.join(dot),capture_output=True,text=True,check=True,timeout=30)
    layout=json.loads(run.stdout);bb=[float(x) for x in layout['bb'].split(',')];height=bb[3]+40
    svg=ET.Element('{'+NS+'}svg',{'xmlns':NS,'viewBox':f'0 0 {bb[2]+40} {height}', 'role':'img','aria-label':'GSN assurance argument', 'data-diagram-type':'gsn-core'})
    # Namespace is supplied by ElementTree, not a second hand-authored attribute.
    svg.attrib.pop('xmlns')
    defs=add(svg,'defs')
    for name,hollow in [('support',False),('context',True)]:
        m=add(defs,'marker',{'id':'gsn-'+name,'markerWidth':11,'markerHeight':10,'refX':10,'refY':5,'orient':'auto','markerUnits':'userSpaceOnUse'})
        add(m,'path',{'d':'M1 1L10 5L1 9Z','fill':'var(--panel)' if hollow else 'var(--arrow)','stroke':'var(--arrow)','stroke-width':1.3})
    for i,e in enumerate(model['edges']):
        row=next((r for r in layout.get('edges',[]) if r.get('id')=='r'+str(i)),None)
        if not row:raise ValueError('GSN relationship is missing from layout')
        points=next((d['points'] for d in row.get('_draw_',[]) if d['op']=='b'),None)
        if not points:raise ValueError('GSN relationship has no route')
        pp=[(x+20,height-y-20) for x,y in points]
        path=f'M{pp[0][0]} {pp[0][1]}'
        if (len(pp)-1)%3==0:
            for j in range(1,len(pp),3):path+=' C'+' '.join(f'{x} {y}' for x,y in pp[j:j+3])
        else:path+=' L'+' '.join(f'{x} {y}' for x,y in pp[1:])
        g=add(svg,'g',{'data-gsn-edge':e['id'],'data-edge-from':e['source'],'data-edge-to':e['target'],'data-edge-kind':e['type']})
        add(g,'title',content=('Supported by' if e['type']=='supported_by' else 'In context of')+': '+ix[e['target']]['title'])
        add(g,'path',{'d':path,'stroke':'var(--arrow)','stroke-width':1.7,'fill':'none','marker-end':'url(#gsn-'+('support' if e['type']=='supported_by' else 'context')+')'})
    objects={o['name']:o for o in layout['objects']}
    for key,n in ix.items():
        row=objects[keys[key]];cx,cy=[float(v) for v in row['pos'].split(',')];cx+=20;cy=height-cy-20;w,h=sizes[key];x=cx-w/2;y=cy-h/2;t=n['type']
        g=add(svg,'g',{'data-node-id':key,'data-node-label':n['title'],'data-gsn-type':t,'tabindex':0,'role':'button','aria-label':'Inspect '+n['title'],'aria-pressed':'false'})
        shape={'fill':'var(--gsn-goal)' if t in ('goal','undeveloped_goal') else 'var(--gsn-strategy)' if t=='strategy' else 'var(--gsn-other)','stroke':'var(--gsn-stroke)','stroke-width':1.6}
        if t=='strategy':add(g,'polygon',dict(shape,points=f'{x+20},{y} {x+w},{y} {x+w-20},{y+h} {x},{y+h}'))
        elif t in ('assumption','justification'):
            add(g,'ellipse',dict(shape,cx=cx,cy=cy,rx=w/2,ry=h/2));label(g,x+w-9,y+h, 'A' if t=='assumption' else 'J',size=16,weight=650)
        elif t=='solution':add(g,'circle',dict(shape,cx=cx,cy=cy,r=w/2))
        else:add(g,'rect',dict(shape,x=x,y=y,width=w,height=h,rx=h/2 if t=='context' else 0))
        label(g,cx,y+25,key,width=25,size=11,weight=600)
        titlelines=lines(n['title'],18 if t=='solution' else 26)
        label(g,cx,cy-(len(titlelines)-1)*10+10,'\n'.join(titlelines),width=30,size=15,weight=550)
        if t=='undeveloped_goal':
            add(g,'path',{'d':f'M{cx} {y+h}l10 10l-10 10l-10 -10Z','fill':'var(--panel)','stroke':'var(--gsn-stroke)','stroke-width':1.6})
    if {g.get('data-gsn-edge') for g in svg.iter() if g.get('data-gsn-edge')}!={e['id'] for e in model['edges']}:raise ValueError('GSN layout lost relationships')
    return ET.tostring(svg,encoding='unicode')


def build(source,output,*,title='Assurance argument',replace=False):
    source=Path(source).resolve();output=Path(output).absolute()
    if output.is_symlink() or source.is_relative_to(output.resolve()):raise ValueError('Output may not contain or alias the source')
    marker=output/'reader.json'
    if output.exists() and (not replace or not marker.is_file() or json.loads(marker.read_text()).get('role')!='gsn-core-reader'):
        raise ValueError('Choose a new output directory or replace an owned GSN reader')
    raw=source.read_bytes();model=json.loads(raw);validate(model)
    payload={'role':'gsn-core-reader','title':title,'model':model,'svg':diagram(model),'sourceSha256':hashlib.sha256(raw).hexdigest()}
    output.parent.mkdir(parents=True,exist_ok=True);lock=output.with_name(output.name+'.reader-lock')
    with lock.open('x'):
        try:
            with tempfile.TemporaryDirectory(dir=output.parent,prefix='.gsn-reader-') as tmp:
                stage=Path(tmp)/'export';stage.mkdir();(stage/'reader.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
                (stage/'assurance-case.json').write_bytes(raw)
                subprocess.run(['node',str(PACKAGE/'gsn-reader.mjs'),str(stage/'reader.json'),str(stage/'index.html')],capture_output=True,text=True,check=True,timeout=60)
                if source.read_bytes()!=raw:raise ValueError('GSN source changed during rendering')
                (stage/'LICENSES.txt').write_text((PACKAGE/'upstream/LICENSE').read_text()+'\n'+(PACKAGE/'upstream/THIRD_PARTY_NOTICES.md').read_text())
                old=Path(tmp)/'previous'
                if output.exists():output.rename(old)
                try:stage.rename(output)
                except BaseException:
                    if old.exists():old.rename(output)
                    raise
        finally:lock.unlink(missing_ok=True)
    return {'ok':True,'html':str(output/'index.html'),'nodes':len(model['nodes']),'relationships':len(model['edges']),'profile':'GSN v3 core subset','browserReview':'pending'}
