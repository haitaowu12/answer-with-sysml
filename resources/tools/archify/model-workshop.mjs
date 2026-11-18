/** Archify shell adapter over a ModelSession. Source authority stays in session. */
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {execFile,spawnSync} from 'node:child_process';
import {promisify} from 'node:util';
import {createHash} from 'node:crypto';
import {applyTemplate,renderCards} from './upstream/renderers/shared/utils.mjs';
const exec=promisify(execFile),here=new URL('.',import.meta.url);
const safe=value=>JSON.stringify(value).replaceAll('<','\\u003c').replaceAll('>','\\u003e').replaceAll('&','\\u0026');
const digest=x=>createHash('sha256').update(x).digest('hex');
export async function workshopPage(session,token){
 const project=session.project,snapshot=session.snapshot,identity=new Map(project.identities.map(i=>[i.locator,i.id])),by=new Map(snapshot.elements.map(e=>[e.locator,e]));
 const recipes=project.views;
 if(!recipes.length)throw Error('A workshop reader requires at least one saved view');
 const views=[],evidence=Object.create(null);
 for(const e of snapshot.elements)evidence[identity.get(e.locator)]={name:e.name,kind:e.kind,file:e.source.document||'Engine-derived declaration',line:e.source.line,endLine:e.source.endLine,excerpt:e.source.text||'Source witness available in native source export.'};
 const temp=await fs.mkdtemp(path.join(os.tmpdir(),'archify-workshop-'));
 try{for(const recipe of recipes){
 const subject=session.resolve(recipe.subject),scope=new Set([subject.locator]);let frontier=[subject.locator];
 for(let i=0;i<recipe.depth;i++){const next=snapshot.elements.filter(e=>frontier.includes(e.owner));next.forEach(e=>scope.add(e.locator));frontier=next.map(e=>e.locator);}
 if(recipe.concern==='types')for(const locator of [...scope]){const type=by.get(locator)?.type?.resolvedId;if(by.has(type))scope.add(type);}
 const elements=snapshot.elements.filter(e=>scope.has(e.locator));
 if(elements.length>45)throw Error('Select a smaller scope: workshop views support 45 visible declarations');
 const nodes=elements.map(e=>({id:identity.get(e.locator),elementId:identity.get(e.locator),selectionKey:'element:'+identity.get(e.locator),readerId:'m'+digest(identity.get(e.locator)).slice(0,24),label:e.name,role:e.kind,metaclass:e.kind,locator:e.locator})),nodeBy=new Map(nodes.map(n=>[n.locator,n]));
 const edges=[];for(const e of elements){const to=nodeBy.get(e.locator),owner=nodeBy.get(e.owner);if(recipe.concern==='structure'&&owner)edges.push({id:'own-'+to.id,elementId:to.id,source:owner.id,target:to.id,kind:'containment',label:'Owned member'});const type=nodeBy.get(e.type?.resolvedId);if(recipe.concern==='types'&&type)edges.push({id:'type-'+to.id,elementId:to.id,source:to.id,target:type.id,kind:'typing',label:'Typed by'});}
 const indices=new Map(nodes.map((n,i)=>[n.id,'n'+i]));
 const dot='digraph G {graph[rankdir=LR,nodesep=0.8,ranksep=1.4];node[shape=box,width=3.1,height=1.4,fixedsize=true,label=""];'+nodes.map(n=>indices.get(n.id)+';').join('')+edges.map(e=>indices.get(e.source)+'->'+indices.get(e.target)+';').join('')+'}';
 const layout=spawnSync('dot',['-Tplain'],{input:dot,encoding:'utf8'});if(layout.status!==0)throw Error('Graphviz layout is unavailable');const coords=new Map(layout.stdout.split('\n').map(l=>l.split(' ')).filter(r=>r[0]==='node').map(r=>[r[1],[Number(r[2])*72,Number(r[3])*72]]));
 const spec={schema_version:1,diagram_type:'architecture',meta:{output:'diagram.html',title:recipe.title||recipe.id,animation:'none',quality_profile:'standard',legend:{mode:'hidden'}},components:nodes.map((n,i)=>{const p=recipe.arrangement?.[n.id];return{id:n.readerId,type:'backend',label:n.label,sublabel:n.role,icon:'none',pos:p?[p.x,p.y]:coords.get(indices.get(n.id)),size:[220,100]}}),connections:edges.map(e=>({id:e.id,from:nodes.find(n=>n.id===e.source).readerId,to:nodes.find(n=>n.id===e.target).readerId,label:''}))};
 const input=path.join(temp,'diagram.json'),output=path.join(temp,'diagram.html');await fs.writeFile(input,JSON.stringify(spec));await exec(process.execPath,[new URL('upstream/bin/archify.mjs',here).pathname,'render','architecture',input,output],{maxBuffer:2**20,cwd:temp});const raw=await fs.readFile(output,'utf8'),svg=raw.match(/<svg\b[^>]*role="img"[\s\S]*?<\/svg>/)?.[0]?.replace(/ marker-(?:start|end)="[^"]*"/g,'');if(!svg)throw Error('Native renderer did not return a drawing');
 const projection={scopeElementId:recipe.subject,statement:'',warnings:[],omissions:[],legendItems:[recipe.concern==='types'?'Lines identify declared types.':'Lines identify ownership. Directed path traversal is disabled for these relation classes.']};
 views.push({id:recipe.id,label:recipe.title||recipe.id,group:'My scoped views',question:recipe.concern==='types'?'Which definitions type these usages?':'What is inside this scope?',scope:subject.locator+' · depth '+recipe.depth+' · '+recipe.concern,family:recipe.concern,sourceSha256:snapshot.hash,projection,nodes,edges,svg,readingRows:[],recipe});
 }
 const data={schemaVersion:1,role:'semantic-model-reader',revision:project.revision,presentation:project.presentation,title:project.title||'Model workshop',sourceSha256:snapshot.hash,results:project.results,source:project.files.map(f=>f.source).join('\n'),evidence,views,modelService:token?{projectId:project.id,presentation:project.presentation,token,revision:project.revision,canUndo:session.canUndo,canRedo:session.canRedo,results:project.results,subjects:project.identities.map(i=>({...i,...by.get(i.locator)})).filter(i=>i.editable!==false)}:null};
 // Reuse the existing reader assembler and native reader; the only extra
 // adapter binds explicit semantic roles and guards directed traversal.
 const input=path.join(temp,'reader.json'),output=path.join(temp,'index.html');await fs.writeFile(input,safe(data));await exec(process.execPath,[new URL('semantic-reader.mjs',here).pathname,input,output],{maxBuffer:2**20});return await fs.readFile(output,'utf8');
 }finally{await fs.rm(temp,{recursive:true,force:true})}
}
