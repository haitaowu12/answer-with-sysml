"""Styled communication renderings for typed SysML v2 view profiles.

Layout is separate from semantic extraction. All model marks retain exact
witnesses; no renderer is allowed to invent a start, success state or result.
"""
import json
import math
import re
import subprocess
import textwrap
import xml.etree.ElementTree as ET

NS='http://www.w3.org/2000/svg'
Q='{'+NS+'}'
ET.register_namespace('',NS)


def el(parent,tag,attrs=None,text=None):
    child=ET.SubElement(parent,Q+tag,{str(k):str(v) for k,v in (attrs or {}).items()})
    child.text=text;return child


def text(parent,x,y,value,*,size=14,anchor='start',color='var(--text)',weight=400,width=32):
    lines=[]
    for line in str(value).split('\n'):lines.extend(textwrap.wrap(line,width=width,break_long_words=True) or [''])
    t=el(parent,'text',{'x':x,'y':y,'font-size':size,'text-anchor':anchor,'fill':color,'font-weight':weight,'font-family':'Inter,system-ui,sans-serif'})
    for i,line in enumerate(lines):el(t,'tspan',{'x':x,'dy':0 if i==0 else size*1.35},line)
    return t


def svg(width,height,label):
    root=ET.Element(Q+'svg',{'viewBox':f'0 0 {width:g} {height:g}','role':'img','aria-label':label,
        'data-diagram-type':'sysml-semantic','preserveAspectRatio':'xMidYMid meet'})
    defs=el(root,'defs')
    for id,color,open in [('semantic-arrow','#52727e',False),('item-arrow','#218997',False),('type-arrow','#52727e',True)]:
        marker=el(defs,'marker',{'id':id,'markerWidth':9,'markerHeight':8,'refX':8,'refY':4,'orient':'auto','markerUnits':'userSpaceOnUse'})
        el(marker,'path',{'d':'M0 0L8 4L0 8Z','fill':'var(--bg)' if open else color,'stroke':color,'stroke-width':1.1})
    return root


def node_group(parent,n):
    return el(parent,'g',{'data-node-id':n['readerId'],'data-node-label':n['label'].replace('\n',' · '),
        'data-model-element':n['elementId'],'data-selection-key':n['selectionKey'],'role':'button',
        'tabindex':0,'aria-label':'Select '+n['label'].replace('\n',' · '),'aria-pressed':'false'})


def relation_group(parent,e):
    return el(parent,'g',{'data-model-relation':e['elementId'],'data-relation-label':e['label'],'data-edge-id':e['id']})


def card(parent,n,x,y,w,h):
    g=node_group(parent,n);role=n['role']
    fill=('var(--semantic-analysis-fill, #e9f1fc)' if role in ('verification','analysis','objective','requirement') else
          'var(--semantic-definition-fill, #f2edfc)' if 'Definition' in n.get('metaclass','') else 'var(--semantic-usage-fill, #e7f4f3)')
    if role in ('ForkNode','JoinNode'):
        el(g,'rect',{'x':x+w*.12,'y':y+h*.43,'width':w*.76,'height':8,'rx':3,'fill':'var(--arrow)'})
        text(g,x+w/2,y+h*.75, 'Fork' if role=='ForkNode' else 'Join',size=11,anchor='middle')
    elif role in ('DecisionNode','MergeNode'):
        el(g,'path',{'d':f'M{x+w/2} {y+6}L{x+w-6} {y+h/2}L{x+w/2} {y+h-6}L{x+6} {y+h/2}Z',
            'fill':fill,'stroke':'var(--arrow)','stroke-width':1.4})
        text(g,x+w/2,y+h/2+4,'Decision' if role=='DecisionNode' else 'Merge',size=11,anchor='middle')
    elif role in ('entry','boundary'):
        el(g,'circle',{'cx':x+w/2,'cy':y+h/2,'r':7,'fill':'var(--arrow)'})
        text(g,x+w/2,y+h/2+27,n['label'],size=11,anchor='middle')
    else:
        definition=n.get('metaclass','').endswith('Definition')
        el(g,'rect',{'x':x,'y':y,'width':w,'height':h,'rx':2 if definition else 10,'fill':fill,
            'stroke':'#91a7af','stroke-width':1.4})
        if role=='parameter' and n.get('direction') in ('in','out'):
            tag=('Input' if n['direction']=='in' else 'Output')
        elif role in ('variation','variant','configuration'):tag={'variation':'Variation','variant':'Variant','configuration':'Selection'}[role]
        else:tag='Definition' if definition else ''
        if tag:text(g,x+14,y+18,tag,size=10,color='var(--semantic-muted, #58727d)',weight=550)
        text(g,x+w/2,y+32 if not tag else y+41,n['label'],size=14,anchor='middle',weight=600,width=max(10,int(w/8)))
        sub=n.get('sublabel') or ''
        if sub and sub.lower()!=n['label'].lower():
            subwidth=max(12,int(w/7)); sublines=sum(max(1,len(textwrap.wrap(line,width=subwidth,break_long_words=True))) for line in sub.split('\n'))
            text(g,x+w/2,y+h-15-(sublines-1)*14.85,sub,size=11,anchor='middle',color='var(--semantic-muted, #58727d)',width=subwidth)
    return g


def graph(projection,nodes,edges):
    """Graphviz computes coordinates only; all visible semantics come from facts."""
    by={n['id']:n for n in nodes};ix={key:'n'+str(i) for i,key in enumerate(by)}
    children={}
    for n in nodes:
        if n.get('parent') in by:children.setdefault(n['parent'],[]).append(n['id'])
    clusters={key for key in children}
    dot=['digraph G {graph[rankdir=LR,nodesep=.55,ranksep=1.0,pad=.35,compound=true,splines=spline];node[shape=box,fixedsize=true,label=""];']
    def add_node(key):
        n=by[key];short=n['role'] in ('ForkNode','JoinNode','DecisionNode','MergeNode','entry','boundary')
        w=.32 if n['role'] in ('entry','boundary') else 1.35 if short else max(2.7,min(4.1,len(n['label'])*.11));h=.72 if short else max(1.05,(35+20*max(1,len(textwrap.wrap(n['label'],width=max(10,int(w*72/8)))) )+15*max(1,len(textwrap.wrap(n.get('sublabel') or '',width=max(12,int(w*72/7)))))+(18 if n.get('direction') or n.get('metaclass','').endswith('Definition') else 0))/72)
        return f'{ix[key]}[width={w},height={h}];'
    def add_cluster(key):
        code=[f'subgraph cluster_{ix[key]} {{graph[label={json.dumps(by[key]["label"])},margin=26];',f'{ix[key]}[width=.1,height=.1,style=invis];']
        for child in children[key]:code.extend(add_cluster(child) if child in clusters else [add_node(child)])
        code.append('}');return code
    for n in nodes:
        if n.get('parent') in clusters:continue
        dot.extend(add_cluster(n['id']) if n['id'] in clusters else [add_node(n['id'])])
    for e in edges:
        compound=('ltail=cluster_'+ix[e['source']]+',' if e['source'] in clusters else '')+('lhead=cluster_'+ix[e['target']]+',' if e['target'] in clusters else '')
        label=e['label'];dot.append(ix[e['source']]+'->'+ix[e['target']]+'['+compound+'id='+json.dumps(e['id'])+',label='+json.dumps(label)+',fontsize=11,arrowhead=none];')
    dot.append('}')
    result=subprocess.run(['dot','-Tjson'],input='\n'.join(dot),text=True,capture_output=True,check=True,timeout=25)
    layout=json.loads(result.stdout);bb=[float(v) for v in layout['bb'].split(',')];height=bb[3]+30
    root=svg(bb[2]+30,height,projection['question'])
    objects={o['name']:o for o in layout['objects']};boxes={}
    for key in clusters:
        obj=objects['cluster_'+ix[key]];box=[float(v) for v in obj['bb'].split(',')]
        x,y,w,h=box[0]+15,height-box[3]-15,box[2]-box[0],box[3]-box[1]
        boxes[key]=(x,y,w,h)
    # Outer frames first, retaining nested scope and concurrent-region labels.
    for key,(x,y,w,h) in sorted(boxes.items(),key=lambda item:-item[1][2]*item[1][3]):
        n=by[key];g=node_group(root,n)
        el(g,'rect',{'x':x,'y':y,'width':w,'height':h,'rx':12,'fill':'var(--bg)','fill-opacity':.75,
            'stroke':'#9dafb8','stroke-width':1.2,'stroke-dasharray':'6 4' if n.get('parallel') else 'none'})
        title=n['label']+(' · concurrent regions' if n.get('parallel') else '')
        text(g,x+16,y+22,title,size=13,weight=600,width=max(18,int(w/8)))
    for e in edges:
        obj=next((row for row in layout.get('edges',[]) if row.get('id')==e['id']),None)
        if not obj:raise ValueError('Relationship is missing from layout')
        g=relation_group(root,e);points=[]
        for operation in obj.get('_draw_',[]):
            if operation.get('op')=='b':points=operation['points'];break
        if not points:raise ValueError('Relationship has no layout path')
        p=[(x+15,height-y-15) for x,y in points];path=f'M{p[0][0]} {p[0][1]}'
        if len(p)>1 and (len(p)-1)%3==0:
            for i in range(1,len(p),3):path+=' C'+' '.join(f'{x} {y}' for x,y in p[i:i+3])
        else:path+=' L'+' '.join(f'{x} {y}' for x,y in p[1:])
        kind=e['kind'];attrs={'d':path,'fill':'none','stroke':'#218997' if kind=='item-flow' else 'var(--arrow)',
            'stroke-width':1.7,'stroke-linejoin':'round'}
        if kind not in ('binding','containment'):attrs['marker-end']='url(#type-arrow)' if kind in ('typing','specialization') else 'url(#item-arrow)' if kind=='item-flow' else 'url(#semantic-arrow)'
        if kind in ('control','typing','allocation','trace','verify'):attrs['stroke-dasharray']='5 4'
        el(g,'path',attrs)
        if e['label'] and 'lp' in obj:
            x,y=[float(v) for v in obj['lp'].split(',')]
            t=text(g,x+15,height-y-15,e['label'],size=11,anchor='middle',width=34)
            t.set('stroke','var(--bg)');t.set('stroke-width','4');t.set('paint-order','stroke')
    for n in nodes:
        if n['id'] in clusters:continue
        obj=objects[ix[n['id']]];x,y=[float(v) for v in obj['pos'].split(',')];w=float(obj['width'])*72;h=float(obj['height'])*72
        card(root,n,x-w/2+15,height-y-h/2-15,w,h)
    return root


def sequence(projection,nodes,edges):
    by={n['id']:n for n in nodes};d=projection['details'];lifelines=d['lifelines'];ranks=d['eventRanks']
    width=max(760,len(lifelines)*260+80);height=max(430,(max(ranks.values(),default=0)+1)*66+150)
    root=svg(width,height,projection['question']);xs={key:140+i*260 for i,key in enumerate(lifelines)}
    for key in lifelines:
        n=by[key];x=xs[key];card(root,n,x-105,25,210,75)
        el(root,'path',{'d':f'M{x} 102V{height-25}','stroke':'#a5b8c0','stroke-dasharray':'5 5','fill':'none'})
    eventxy={}
    for key,rank in ranks.items():
        n=by[key];x=xs[n['parent']];y=135+rank*66;eventxy[key]=(x,y)
        g=node_group(root,n);el(g,'circle',{'cx':x,'cy':y,'r':4,'fill':'#218997'})
        text(g,x-10,y+5,n['label'],size=10,anchor='end',width=18,color='var(--semantic-muted, #58727d)')
    for edge in edges:
        if edge['kind']!='message':
            a=eventxy[edge['source']];b=eventxy[edge['target']];g=relation_group(root,edge)
            el(g,'path',{'d':f'M{a[0]} {a[1]+5}L{b[0]} {b[1]-7}', 'stroke':'#9aabb4','stroke-width':1.3,'stroke-dasharray':'3 4','fill':'none','marker-end':'url(#semantic-arrow)'})
            continue
        a=eventxy[edge['source']];b=eventxy[edge['target']];g=relation_group(root,edge)
        path=f'M{a[0]} {a[1]}L{b[0]} {b[1]}'
        if a[0]==b[0]:path=f'M{a[0]} {a[1]}H{a[0]+100}V{b[1]}H{b[0]}'
        el(g,'path',{'d':path,'stroke':'#52727e','stroke-width':1.6,'fill':'none','marker-end':'url(#semantic-arrow)'})
        text(g,(a[0]+b[0])/2+(110 if a[0]==b[0] else 0),(a[1]+b[1])/2-12,edge['label'],size=12,anchor='start' if a[0]==b[0] else 'middle',weight=550,width=22)
    return root


def geometry(projection,nodes,edges):
    shapes=projection['details']['shapes'];by={n['id']:n for n in nodes};root=svg(850,max(430,len(shapes)*400),projection['question'])
    for i,shape in enumerate(shapes):
        n=by[shape['nodeId']];d=shape['dimensions'];scale=min(140,390/d['length'],230/d['height']);x=165;y=335+i*400
        w=d['length']*scale;h=d['height']*scale;dx=d['width']*scale*.6;dy=-d['width']*scale*.36
        g=node_group(root,n)
        for points,fill in [([(x,y),(x+w,y),(x+w,y-h),(x,y-h)],'#d7e9ed'),
             ([(x,y-h),(x+dx,y-h+dy),(x+w+dx,y-h+dy),(x+w,y-h)],'#e8f4f3'),
             ([(x+w,y),(x+w+dx,y+dy),(x+w+dx,y-h+dy),(x+w,y-h)],'#b9d4dd')]:
            el(g,'polygon',{'points':' '.join(f'{a},{b}' for a,b in points),'fill':fill,'stroke':'#6d919e','stroke-width':1.5})
        text(g,x,35+i*400,n['label'],size=20,weight=600)
        text(g,x,y+32,f'Length {d["length"]:g} m',size=13)
        text(g,x+w+dx+20,y-h/2,f'Height {d["height"]:g} m',size=13,width=18)
        text(g,x+w+dx/2+20,y-h+dy-18,f'Width {d["width"]:g} m',size=13,width=18)
        text(g,x,65+i*400,'Declared envelope · local shape',size=12,color='var(--semantic-muted, #58727d)')
    return root


def timing(projection,nodes,edges):
    spans=projection['details']['spans'];by={n['id']:n for n in nodes};end=max(s['start']+s['duration'] for s in spans)
    if end<=0:raise ValueError('Timing budget must have a positive extent')
    root=svg(920,145+len(spans)*88,projection['question']);left=270;scale=570/end
    for tick in range(6):
        value=end*tick/5;x=left+scale*value
        el(root,'path',{'d':f'M{x} 58V{100+len(spans)*88}','stroke':'#d8e4e8','stroke-width':1})
        text(root,x,39,f'{value:g} s',size=11,anchor='middle',color='var(--semantic-muted, #58727d)')
    for i,span in enumerate(spans):
        n=by[span['nodeId']];y=88+i*88;g=node_group(root,n)
        text(g,25,y+25,n['label'],size=15,weight=550,width=26)
        x=left+span['start']*scale;w=max(4,span['duration']*scale)
        el(g,'rect',{'x':x,'y':y,'width':w,'height':44,'rx':8,'fill':'#c7e6e6','stroke':'#69a2aa','stroke-width':1.3})
        text(g,x+8,y+27,f'{span["duration"]:g} s',size=13,weight=550)
    return root


def render(projection,nodes,edges):
    mode=projection['presentation']
    renderer={'sequence':sequence,'geometry':geometry,'timing':timing}.get(mode,graph)
    root=renderer(projection,nodes,edges)
    # Structural correspondence is checked after layout, including contextual
    # parameter identities. Browser/matrix marks are checked by the shell data.
    seen={e.get('data-node-id') for e in root.iter() if e.get('data-node-id')}
    if seen!={n['readerId'] for n in nodes}:raise ValueError('Custom layout changed the semantic node set')
    seen_edges={e.get('data-model-relation') for e in root.iter() if e.get('data-model-relation')}
    if seen_edges!={e['elementId'] for e in edges}:raise ValueError('Custom layout changed the semantic relationship set')
    from sysml_reader_binding import bind
    bind(root,nodes,edges,view_id=projection.get('id',projection['viewKind']),revision=projection.get('sourceSha256',''))
    return ET.tostring(root,encoding='unicode')
