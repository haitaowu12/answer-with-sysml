/** Revisioned source authority. Renderers consume snapshots; they never write sources.
 * A kernel must parse complete source sets, apply semantic operations and verify
 * their postconditions. This module accepts no raw SVG/graph-as-model mutation.
 */
import {createHash, randomUUID} from 'node:crypto';
import {checkResultBasis,evaluateProject} from './model-evaluation.mjs';
export const MAX_PROJECT_BYTES=8*1024*1024;
const clone = x => structuredClone(x);
const hash = x => createHash('sha256').update(JSON.stringify(x)).digest('hex');
const demand = (condition,message) => {if (!condition) throw Error(message);};
const identity = () => 'element-'+randomUUID();
function checkPresentation(presentation,views){
  if(presentation===undefined)return;
  demand(presentation&&typeof presentation==='object'&&!Array.isArray(presentation)&&JSON.stringify(presentation).length<=262144,'Invalid saved reading state');
  if(presentation.states===undefined)return;
  demand(presentation.states&&typeof presentation.states==='object'&&!Array.isArray(presentation.states),'Invalid reading-state map');
  const names=new Set(views.map(v=>v.id));
  for(const [view,text] of Object.entries(presentation.states)){
    demand(names.has(view)&&typeof text==='string'&&text.length<=8192,'Invalid saved view reading state');
    let state;try{state=JSON.parse(text)}catch(_){throw Error('Invalid saved reading state JSON')}
    demand(state?.version===1&&(state.focus==null||typeof state.focus==='string'||Array.isArray(state.focus)&&state.focus.every(x=>typeof x==='string')),'Invalid saved focus');
    demand(state.lens==null||Array.isArray(state.lens)&&state.lens.length<=2&&state.lens.every(x=>typeof x==='string'),'Invalid saved lens');
    demand(state.camera==null||typeof state.camera==='object'&&typeof state.camera.scale==='number'&&state.camera.scale>0&&[state.camera.scale,state.camera.x,state.camera.y].every(Number.isFinite),'Invalid saved camera');
    demand(state.collapsed==null||Array.isArray(state.collapsed)&&state.collapsed.every(x=>typeof x==='string'),'Invalid saved collapse state');
  }
}
export function admitProject(value) {
  const p=clone(value);
  demand(p?.schemaVersion===1 && typeof p.id==='string' && p.id && Array.isArray(p.files) && p.files.length>0 && p.files.length<=64,'Invalid source project');
  demand(Number.isSafeInteger(p.revision) && p.revision>=0,'Invalid project revision');
  demand(p.presentationRevision===undefined||Number.isSafeInteger(p.presentationRevision)&&p.presentationRevision>=0,'Invalid presentation revision');
  const paths=new Set();let bytes=0;
  for(const f of p.files){demand(typeof f.path==='string' && f.path.endsWith('.sysml') && !f.path.startsWith('/') && !/[\\:\u0000-\u001f]/.test(f.path) && Buffer.from(f.path).toString('utf8')===f.path && f.path.split('/').every(x=>x && x!=='.' && x!=='..') && !paths.has(f.path) && typeof f.source==='string' && Buffer.from(f.source).toString('utf8')===f.source,'Invalid or duplicate source path');paths.add(f.path);bytes+=Buffer.byteLength(f.source);}
  demand(bytes<=524288,'Source set exceeds 512 KiB');
  p.views??=[];demand(Array.isArray(p.views)&&p.views.length<=30,'A project supports up to 30 saved views');p.identities??=[];p.results??=[];p.context??={facts:[],choices:[],assumptions:[],questions:[],decisions:[]};p.libraries??=[];p.links??=[];
  const viewIds=new Set();for(const v of p.views){demand(v && typeof v.id==='string' && !viewIds.has(v.id) && typeof v.subject==='string' && ['structure','types'].includes(v.concern) && Number.isInteger(v.depth) && v.depth>=1 && v.depth<=4,'Invalid view recipe');viewIds.add(v.id);v.arrangement??={};demand(v.arrangement&&typeof v.arrangement==='object'&&!Array.isArray(v.arrangement),'Arrangement must be a coordinate record');for(const position of Object.values(v.arrangement))demand(position&&typeof position==='object'&&typeof position.x==='number'&&typeof position.y==='number'&&Number.isFinite(position.x)&&Number.isFinite(position.y),'Arrangement coordinates must be finite');}
  const elementIds=new Set(),locators=new Set();for(const i of p.identities){demand(typeof i.id==='string' && !elementIds.has(i.id) && typeof i.locator==='string' && !locators.has(i.locator),'Invalid identity map');elementIds.add(i.id);locators.add(i.locator);}
  demand(new Set(p.results.map(r=>r.id)).size===p.results.length,'Duplicate result identity');
  for(const r of p.results)demand(typeof r.id==='string' && Array.isArray(r.dependsOn) && r.dependsOn.every(x=>typeof x==='string'),'Invalid result dependencies');
  checkPresentation(p.presentation,p.views);
  demand(Buffer.byteLength(JSON.stringify({...p,history:{undo:[],redo:[]}},null,2)+'\n')<=MAX_PROJECT_BYTES,'Project metadata exceeds the 8 MiB storage budget');
  return p;
}
export class ModelSession {
  #project;#kernel;#snapshot;#undo=[];#redo=[];#busy=false;
  static async open(project,kernel){const session=new ModelSession();session.#project=admitProject(project);const history=session.#project.history;delete session.#project.history;if(history){demand(Array.isArray(history.undo)&&Array.isArray(history.redo)&&history.undo.length<=20&&history.redo.length<=20,'Invalid project history');session.#undo=history.undo.map(project=>({project:admitProject(project),snapshot:null}));session.#redo=history.redo.map(project=>({project:admitProject(project),snapshot:null}));demand([...session.#undo,...session.#redo].every(r=>r.project.id===session.#project.id&&!r.project.history),'History belongs to another project or contains nested histories');}session.#kernel=kernel;if(kernel.authority){demand(!session.#project.authority||hash(session.#project.authority)===hash(kernel.authority),'Project source authority differs from the configured kernel');session.#project.authority=clone(kernel.authority);}session.#snapshot=await kernel.parse(session.#project.files,session.#project.libraries);session.#reconcile();session.#checkViews();checkResultBasis(session.#project);return session;}
  get project(){return clone(this.#project)}
  get snapshot(){return clone(this.#snapshot)}
  get canUndo(){return this.#undo.length>0}
  get canRedo(){return this.#redo.length>0}
  #reconcile(){const available=new Set(this.#snapshot.elements.map(e=>e.locator));demand(this.#project.identities.every(i=>available.has(i.locator)),'Stored model identity is unresolved; explicit reference repair is required');const old=new Map(this.#project.identities.map(i=>[i.locator,i]));this.#project.identities=this.#snapshot.elements.map(e=>old.get(e.locator)||{id:identity(),locator:e.locator});}
  #checkViews(){this.#checkReferences(this.#project);}
  #checkReferences(project){const ids=new Set(project.identities.map(i=>i.id));for(const v of project.views){demand(ids.has(v.subject),'Saved view subject is unresolved');demand(Object.keys(v.arrangement).every(id=>ids.has(id)),'Arrangement identity is unresolved');}for(const r of project.results)demand(r.dependsOn.every(id=>ids.has(id)),'Result dependency is unresolved');}
  resolve(id){const entry=this.#project.identities.find(i=>i.id===id);demand(entry,'Unknown persistent model identity');const element=this.#snapshot.elements.find(e=>e.locator===entry.locator);demand(element,'Model identity needs reference repair');return clone({...element,id});}
  #revision(base){demand(base===this.#project.revision,'Stale base revision');}
  async #exclusive(action){demand(!this.#busy,'A model transaction is already in progress');this.#busy=true;try{return await action()}finally{this.#busy=false}}
  async apply(command){return this.#exclusive(async()=>{
    this.#revision(command.baseRevision);const before=this.project;
    const operations=command.operations;demand(Array.isArray(operations)&&operations.length>0&&operations.length<=20,'Provide 1–20 typed operations');
    const resolved=operations.map(op=>{demand(['rename','set-value'].includes(op.type),'Unsupported semantic operation');const target=this.resolve(op.target);demand(target.editable!==false,'This generated object has no editable source declaration');demand(op.context===undefined,'This edit profile does not support occurrence context');
      if(op.type==='rename')demand(/^[A-Za-z_][A-Za-z0-9_]*$/.test(op.name),'Use an unquoted SysML identifier');
      if(op.type==='set-value')demand(typeof op.value==='number'&&Number.isFinite(op.value),'This profile edits finite numeric typed values');
      return {...clone(op),locator:target.locator,kind:target.kind};});
    demand(new Set(resolved.map(o=>o.target)).size===resolved.length,'One operation per target in this edit profile');
    // Referenced targets are resolved against the same accepted revision. A
    // rename plus a descendant edit needs a sequential transaction, not guesses.
    for(const a of resolved)for(const b of resolved)if(a!==b&&a.type==='rename')demand(!b.locator.startsWith(a.locator+'::'),'Overlapping rename targets require separate transactions');
    const candidate=await this.#kernel.edit(before.files,resolved,this.#snapshot,before.libraries);
    demand(candidate.files.some(f=>f.source!==before.files.find(b=>b.path===f.path)?.source),'The command produced no source change');
    const applied=new Set(candidate.applied);
    demand(applied.size===resolved.length&&resolved.every((_,i)=>applied.has(i)),'Kernel did not apply the complete requested operation set');
    const migrate=locator=>{const op=resolved.find(o=>o.type==='rename'&&(locator===o.locator||locator.startsWith(o.locator+'::')));return op?(op.locator.includes('::')?op.locator.slice(0,op.locator.lastIndexOf('::')+2):'')+op.name+locator.slice(op.locator.length):locator;};
    demand(candidate.snapshot.elements.length===this.#snapshot.elements.length,'Kernel changed the declaration set outside the command profile');
    await this.#kernel.verify(this.#snapshot,candidate.snapshot,resolved,migrate);
    const next=admitProject({...before,files:candidate.files,revision:before.revision+1});
    demand(next.files.length===before.files.length&&before.files.every(f=>next.files.some(n=>n.path===f.path)),'Kernel changed source-set membership');
    next.identities=before.identities.map(i=>({...i,locator:migrate(i.locator)}));
    const locators=new Set(candidate.snapshot.elements.map(e=>e.locator));demand(next.identities.every(i=>locators.has(i.locator))&&new Set(next.identities.map(i=>i.locator)).size===next.identities.length,'Identity migration is incomplete or ambiguous');
    const changedIds=new Set(resolved.map(o=>o.target));
    const consequences=[];
    for(const view of next.views){view.status='refresh';consequences.push({kind:'regenerate',viewId:view.id,reason:'Accepted model revision changed'});}
    for(const result of next.results)if(result.receipt||result.expression&&changedIds.has(result.expression)||result.dependsOn.some(id=>changedIds.has(id))){result.status='stale';result.staleAgainstRevision=next.revision;consequences.push({kind:'recompute',resultId:result.id,reason:'An explicit input dependency changed'});}
    for(const link of next.links)if(changedIds.has(link.source)||changedIds.has(link.target))consequences.push({kind:link.role==='evidence'?'review':'revalidate',linkId:link.id,reason:'A linked engineering object changed'});
    next.lastChange={id:command.id||randomUUID(),baseRevision:before.revision,revision:next.revision,operations:resolved,files:next.files.filter(f=>f.source!==before.files.find(b=>b.path===f.path).source).map(f=>f.path),consequences};
    admitProject(next);
    await this.#kernel.validateProject?.(next,candidate.snapshot);
    this.#undo.push({project:before,snapshot:this.#snapshot});this.#redo=[];this.#project=next;this.#snapshot=candidate.snapshot;this.#reconcile();this.#checkViews();return this.project;
  });}
  async evaluate(baseRevision,resultId){return this.#exclusive(async()=>{
    this.#revision(baseRevision);const before=this.project;
    const next=admitProject(await evaluateProject(before,this.#snapshot,this.#kernel,id=>this.resolve(id),resultId));
    this.#checkReferences(next);checkResultBasis(next);
    await this.#kernel.validateProject?.(next,this.#snapshot);
    this.#undo.push({project:before,snapshot:this.#snapshot});this.#redo=[];this.#project=next;return this.project;
  });}
  async arrange(baseRevision,viewId,patch){return this.#exclusive(async()=>{this.#revision(baseRevision);const next=this.project,view=next.views.find(v=>v.id===viewId);demand(view,'Unknown saved view');for(const [id,position] of Object.entries(patch)){this.resolve(id);demand(Number.isFinite(position.x)&&Number.isFinite(position.y),'Arrangement coordinates must be finite');Object.defineProperty(view.arrangement,id,{value:{x:position.x,y:position.y},writable:true,enumerable:true,configurable:true});}next.revision++;admitProject(next);await this.#kernel.validateProject?.(next,this.#snapshot);this.#undo.push({project:this.project,snapshot:this.#snapshot});this.#redo=[];this.#project=next;return this.project;});}
  async savePresentation(baseRevision,presentation){return this.#exclusive(async()=>{this.#revision(baseRevision);checkPresentation(presentation,this.#project.views);const next=this.project;next.presentation=clone(presentation);next.presentationRevision=(next.presentationRevision||0)+1;admitProject(next);this.#project=next;return this.project;});}
  async saveView(baseRevision,recipe){return this.#exclusive(async()=>{this.#revision(baseRevision);const next=this.project;demand(!next.views.some(v=>v.id===recipe.id),'Saved view already exists');next.views.push(clone(recipe));next.revision++;const checked=admitProject(next);this.resolve(recipe.subject);await this.#kernel.validateProject?.(checked,this.#snapshot);this.#undo.push({project:this.project,snapshot:this.#snapshot});this.#redo=[];this.#project=checked;return this.project;});}
  async #history(base,direction){return this.#exclusive(async()=>{
    this.#revision(base);
    const from=direction==='undo'?this.#undo:this.#redo,to=direction==='undo'?this.#redo:this.#undo;
    demand(from.length,'No '+direction+' available');
    const next=admitProject({...clone(from.at(-1).project),revision:this.#project.revision+1});
    if(this.#kernel.authority)demand(hash(next.authority)===hash(this.#kernel.authority),'History source authority differs from the configured kernel');
    const snapshot=await this.#kernel.parse(next.files,next.libraries);
    const locators=new Set(snapshot.elements.map(e=>e.locator)),ids=new Set(next.identities.map(i=>i.id));
    demand(next.identities.every(i=>locators.has(i.locator)),'History model identity is unresolved; explicit reference repair is required');
    demand(next.views.every(v=>ids.has(v.subject)),'History view subject is unresolved');
    this.#checkReferences(next);checkResultBasis(next);
    // History is a candidate transaction too. Validate before changing either
    // stack or accepted state, including after reopening imported history.
    await this.#kernel.validateProject?.(next,snapshot);
    to.push({project:this.project,snapshot:this.#snapshot});from.pop();
    this.#project=next;this.#snapshot=snapshot;return this.project;
  });}
  undo(base){return this.#history(base,'undo')}
  redo(base){return this.#history(base,'redo')}
  export(){
    const history={undo:this.#undo.slice(-20).map(r=>r.project),redo:this.#redo.slice(-20).map(r=>r.project)};
    let value;
    for(;;){
      value=JSON.stringify({...this.#project,history},null,2)+'\n';
      if(Buffer.byteLength(value)<=MAX_PROJECT_BYTES)return value;
      demand(history.undo.length||history.redo.length,'Project exceeds the 8 MiB storage budget');
      // Keep nearest undo/redo states. Large native source sets retain fewer
      // snapshots so every exported project fits the running reopen route.
      (history.undo.length>=history.redo.length?history.undo:history.redo).shift();
    }
  }
  digest(){return hash(this.#project.files)}
}
