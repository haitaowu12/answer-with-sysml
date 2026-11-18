/** Explicit evaluation of a saved declared expression, never user-supplied code.
 * A receipt describes a local computation, not requirement/evidence acceptance.
 */
import {createHash} from 'node:crypto';
const hash=value=>createHash('sha256').update(JSON.stringify(value)??'null').digest('hex');
const demand=(ok,message)=>{if(!ok)throw Error(message)};
export function numericResult(result){
 demand(result&&['int','real'].includes(result.kind)&&typeof result.value==='number'&&Number.isFinite(result.value)&&(result.kind!=='int'||Number.isSafeInteger(result.value)),'Evaluation requires a finite numeric result without integer precision loss');
 return {kind:result.kind,value:result.value};
}
export function checkResultBasis(project){
 const digest=hash(project.files),byId=new Map(project.identities.map(i=>[i.id,i.locator]));
 for(const result of project.results){
  if(result.expression===undefined)continue; // Legacy supplied results retain their explicit-dependency contract.
  demand(typeof result.expression==='string'&&byId.has(result.expression),'Result expression is unresolved');
  const receipt=result.receipt;
  const matches=receipt?.schemaVersion===1&&receipt.sourceDigest===digest&&hash(receipt.authority)===hash(project.authority)&&receipt.expression?.id===result.expression&&receipt.expression.locator===byId.get(result.expression)&&receipt.value===result.value&&['int','real'].includes(receipt.kind)&&Number.isFinite(receipt.value)&&(receipt.kind!=='int'||Number.isSafeInteger(receipt.value))&&Array.isArray(receipt.inputs)&&receipt.inputs.length===result.dependsOn.length&&receipt.inputs.every((input,i)=>input.id===result.dependsOn[i]&&input.locator===byId.get(input.id));
  if(result.status==='current'&&!matches){result.status='stale';result.staleReason='The stored calculation basis does not match this source, expression, inputs or engine. Evaluate again.';}
 }
}
export async function evaluateProject(project,snapshot,kernel,resolve,resultId){
 const next=structuredClone(project),result=next.results.find(r=>r.id===resultId);
 demand(result,'Unknown saved result');demand(result.expression,'This result has no declared expression');demand(typeof kernel.evaluate==='function'&&kernel.authority,'The configured kernel does not support witnessed numeric evaluation');
 const expression=resolve(result.expression);
 const inputs=[];
 for(const id of result.dependsOn){const input=resolve(id),value=numericResult(await kernel.evaluate(snapshot,input.locator));inputs.push({id,locator:input.locator,source:input.source,...value});}
 const value=numericResult(await kernel.evaluate(snapshot,expression.locator));
 result.receipt={schemaVersion:1,sourceDigest:hash(project.files),acceptedRevision:project.revision,authority:structuredClone(kernel.authority),expression:{id:result.expression,locator:expression.locator,source:expression.source},inputs,...value};
 result.value=value.value;result.status='current';delete result.staleAgainstRevision;delete result.staleReason;
 next.revision++;next.lastChange={baseRevision:project.revision,revision:next.revision,operations:[{type:'evaluate',resultId,expression:result.expression}],files:[],consequences:[]};
 return next;
}
