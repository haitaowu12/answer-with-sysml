/** Service-backed OpenSysML adapter. Connection and runtime pin are explicit.
 * This uses ApplyEdits, not the narrower connectWasm interface. API JSON is a
 * bounded experimental reference witness, never an interchange authority.
 */
import {authorizeEditWitnesses} from './model-edit-witness.mjs';
const demand=(ok,message)=>{if(!ok)throw Error(message)};
const clone=x=>structuredClone(x);
function references(rows){const triples=[];function visit(value,path,owner){if(Array.isArray(value)){value.forEach((item,i)=>visit(item,path+'['+i+']',owner));return}if(!value||typeof value!=='object')return;if(typeof value['@id']==='string')triples.push([owner,path,value['@id']]);for(const [key,item] of Object.entries(value))if(key!=='@id')visit(item,path+'.'+key,owner)}for(const row of rows)for(const [key,value] of Object.entries(row))if(key!=='@id')visit(value,key,row['@id']);return triples;}
export function openSysMLKernel(connection){
  const models=new Map();
  async function parse(files,libraries=[]){
    demand(libraries.length===0,'External library overlays require a configured pinned source-set adapter');
    const model=await connection.parseSources(files.map(f=>[f.path,f.source]));model.raiseForErrors();
    const api=JSON.parse((await model.toApiJson()).content);demand(Array.isArray(api),'Expected API reference witness');
    const named=api.filter(row=>typeof row.qualifiedName==='string'&&row.qualifiedName);
    const roots=model.roots.flatMap((r,i)=>r.childIds.map(id=>({id,path:files[i]?.path})));
    const elements=[];
    for(const row of named){const symbol=await model.find(row.qualifiedName)||{name:row.declaredName||row.qualifiedName.split('::').at(-1),kind:row['@type'],attributes:[],type:null};elements.push({locator:row.qualifiedName,name:symbol.name,kind:symbol.kind,editable:Number.isInteger(row['sysx:sourceLine'])&&typeof row.declaredName==='string',type:symbol.type||null,valueEditable:/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(api.find(r=>r['@id']===row.value?.['@id'])?.['sysx:sourceText']?.trim()||''),attributes:JSON.parse(JSON.stringify(symbol.attributes,(_,value)=>typeof value==='bigint'?value.toString():value)),owner:api.find(r=>r['@id']===row.owner?.['@id'])?.qualifiedName||null,source:{document:roots.filter(r=>row.qualifiedName===r.id||row.qualifiedName.startsWith(r.id+'::')).map(r=>r.path).filter((x,i,a)=>a.indexOf(x)===i).length===1?roots.find(r=>row.qualifiedName===r.id||row.qualifiedName.startsWith(r.id+'::'))?.path:null,line:row['sysx:sourceLine'],endLine:row['sysx:sourceEndLine'],text:row['sysx:sourceText']||''}});}
    for(const e of elements){const file=files.find(f=>f.path===e.source.document);if(file&&Number.isInteger(e.source.line))e.source.text=file.source.split('\n').slice(e.source.line-1,e.source.endLine).join('\n');}
    demand(new Set(elements.map(e=>e.locator)).size===elements.length,'Ambiguous source declarations');
    const snapshot={hash:model.hash,elements,apiRows:api,apiNamed:named.map(r=>({locator:r.qualifiedName,id:r['@id']})),references:references(api)};models.set(model.hash,model);return snapshot;
  }
  async function edit(files,operations,snapshot,libraries){
    const model=models.get(snapshot.hash);demand(model,'Accepted kernel snapshot is unavailable');
    const wire=operations.map(o=>o.type==='rename'?['rename',o.locator,o.name]:['set_value',o.locator,String(o.value)]);
    // Multi-document edits return only changed documents. Merge them into the
    // original set; untouched sources, comments, folders and imports survive.
    const documents=new Set(operations.map(o=>snapshot.elements.find(e=>e.locator===o.locator)?.source.document));
    demand(documents.size===1&&!documents.has(null)&&!documents.has(undefined),'This edit batch requires targets in one unambiguous source document');
    const result=await connection.applyEdits(model.hash,wire,{acceptDocuments:true,document:[...documents][0]});
    demand(!result.diagnostics.some(d=>d.severity==='error'),'Kernel rejected the requested change');
    authorizeEditWitnesses(files,operations,snapshot,result.applied);
    const names=new Set(files.map(f=>f.path)),changed=new Map();for(const document of result.documents){demand(names.has(document.name)&&!changed.has(document.name),'Kernel returned an unknown or duplicate document');changed.set(document.name,document.content);}
    const candidate=files.map(f=>({...f,source:changed.get(f.path)??f.source}));
    // Exact edit witnesses are checked against original UTF-8 bytes. They must
    // reconstruct each returned file completely; unreported changes are refused.
    for(const f of files){const edits=result.applied.filter(e=>e.document===f.path).sort((a,b)=>b.offset-a.offset);let bytes=Buffer.from(f.source),right=bytes.length;for(const e of edits){demand(Number.isInteger(e.operationIndex)&&e.operationIndex>=0&&e.operationIndex<operations.length,'Unknown applied operation');demand(e.offset>=0&&e.length>=0&&e.offset+e.length<=right,'Overlapping or invalid source edit witness');demand(bytes.subarray(e.offset,e.offset+e.length).toString()===e.oldText,'Source edit witness differs from accepted bytes');bytes=Buffer.concat([bytes.subarray(0,e.offset),Buffer.from(e.newText),bytes.subarray(e.offset+e.length)]);right=e.offset;}demand(bytes.equals(Buffer.from(candidate.find(n=>n.path===f.path).source)),'Kernel changed source outside its edit witnesses');}
    return {files:candidate,applied:[...new Set(result.applied.map(e=>e.operationIndex))],snapshot:await parse(candidate,libraries)};
  }
  async function verify(before,after,operations,migrate){
    const afterBy=new Map(after.elements.map(e=>[e.locator,e]));
    demand(before.elements.length===after.elements.length,'This edit profile cannot add or lose engineering declarations');
    for(const old of before.elements){const next=afterBy.get(migrate(old.locator));demand(next&&next.kind===old.kind,'A declaration was lost or retargeted');demand((next.type?.resolvedId||'')===migrate(old.type?.resolvedId||''),'A type reference was silently retargeted');}
    const ids=before.apiNamed.map(old=>{const next=after.apiNamed.find(n=>n.locator===migrate(old.locator));demand(next,'Missing API identity after edit');return[old.id,next.id]}).sort((a,b)=>b[0].length-a[0].length);
    const mapped=id=>{const match=ids.find(([old])=>id===old||id.startsWith(old+'_'));return match?match[1]+id.slice(match[0].length):id;};
    const canonical=refs=>JSON.stringify(refs.map(r=>JSON.stringify(r)).sort());
    demand(canonical(before.references.map(([a,k,b])=>[mapped(a),k,mapped(b)]))===canonical(after.references),'A source reference was lost or retargeted');
    const model=models.get(after.hash);
    for(const op of operations){const target=migrate(op.locator),element=afterBy.get(target);demand(element,'Requested target is missing after edit');
      if(op.type==='rename')demand(element.name===op.name,'Rename postcondition failed');
      else{const value=await model.eval(target);demand(['int','real'].includes(value.kind)&&(value.kind!=='int'||Number.isSafeInteger(op.value))&&Number(value.value)===op.value,'Typed value postcondition failed');}
    }
  }
  async function evaluate(snapshot,locator){
    const model=models.get(snapshot.hash),row=snapshot.apiRows.find(r=>r.qualifiedName===locator);
    demand(model&&row?.value?.['@id'],'Evaluation requires an existing declared value expression');
    const result=await model.eval(locator);
    demand(['int','real'].includes(result.kind),'The declared expression has no supported numeric result');
    const value=Number(result.value);
    demand(Number.isFinite(value)&&(result.kind!=='int'||Number.isSafeInteger(value)&&BigInt(value)===BigInt(result.value)),'Evaluation result is nonfinite or exceeds integer precision');
    return {kind:result.kind,value};
  }
  return {authority:{engine:'OpenSysML',version:'v0.10.0',sourceCommit:'08ef397841767b829e492bbecf6d723483b4421e',adapter:'archify-source-edit-v1'},parse,edit,verify,evaluate};
}
