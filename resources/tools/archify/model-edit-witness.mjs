/** Check edit authorization against accepted semantic identities and byte ranges.
 * Lexical scanning locates unquoted identifier spellings; the engine's typed
 * facts and reference witness remain the semantic authority.
 */
const demand=(ok,message)=>{if(!ok)throw Error(message)};
const validText=s=>typeof s==='string'&&Buffer.from(s).toString('utf8')===s;
function span(file,row){
 const positions=['sysx:sourceLine','sysx:sourceColumn','sysx:sourceEndLine','sysx:sourceEndColumn'].map(k=>row[k]);
 if(!positions.every(n=>Number.isInteger(n)&&n>0))return null;
 const bytes=Buffer.from(file.source),starts=[0];for(let i=0;i<bytes.length;i++)if(bytes[i]===10)starts.push(i+1);
 const [line,column,endLine,endColumn]=positions,start=starts[line-1]+column-1,end=starts[endLine-1]+endColumn-1;
 return Number.isInteger(start)&&Number.isInteger(end)&&start>=0&&end>start&&end<=bytes.length?{start,end}:null;
}
function identifiers(source){
 const result=[];let i=0;
 while(i<source.length){
  if(source.startsWith('//',i)){const end=source.indexOf('\n',i+2);i=end<0?source.length:end;continue}
  if(source.startsWith('/*',i)){const end=source.indexOf('*/',i+2);demand(end>=0,'Unclosed source comment');i=end+2;continue}
  if(source[i]==='"'||source[i]==="'"){const quote=source[i++];while(i<source.length){if(source[i]==='\\'){i+=2;continue}if(source[i++]===quote)break}continue}
  // A numeric token owns its exponent/base suffix. Its letters cannot supply
  // rename authority, even inside the target declaration's wider source span.
  if(/[0-9]/.test(source[i])||source[i]==='.'&&/[0-9]/.test(source[i+1]||'')){
   const number=/^(?:0[xX][A-Fa-f0-9_]+|(?:\d[\d_]*(?:\.[\d_]*)?|\.\d[\d_]*)(?:[eE][+-]?[\d_]+)?)/.exec(source.slice(i));
   i+=number[0].length;continue;
  }
  if(/[A-Za-z_]/.test(source[i])){const start=i++;while(i<source.length&&/[A-Za-z0-9_]/.test(source[i]))i++;result.push({text:source.slice(start,i),start:Buffer.byteLength(source.slice(0,start)),end:Buffer.byteLength(source.slice(0,i))});}else i++;
 }
 return result;
}
function references(value,target){if(Array.isArray(value))return value.some(v=>references(v,target));if(!value||typeof value!=='object')return false;return value['@id']===target||Object.values(value).some(v=>references(v,target));}
export function authorizeEditWitnesses(files,operations,snapshot,edits){
 demand(Array.isArray(edits),'Missing edit witnesses');
 const rows=snapshot.apiRows||[],byId=new Map(rows.map(r=>[r['@id'],r])),byName=new Map(rows.filter(r=>r.qualifiedName).map(r=>[r.qualifiedName,r]));
 const fileBy=new Map(files.map(f=>[f.path,f])),elementBy=new Map(snapshot.elements.map(e=>[e.locator,e]));
 const bounds=row=>{let owner=row;const seen=new Set();while(owner&&!seen.has(owner['@id'])){seen.add(owner['@id']);const file=fileBy.get(elementBy.get(owner.qualifiedName)?.source.document);if(file){const range=span(file,row)||span(file,owner);if(range)return{document:file.path,...range}}owner=byId.get(owner.owner?.['@id']||owner.owningNamespace?.['@id'])}return null;};
 const permitted=operations.map(op=>{
  const row=byName.get(op.locator);demand(row,'No accepted source witness for the requested target');
  if(op.type==='set-value'){
   const file=fileBy.get(elementBy.get(op.locator)?.source.document),range=file&&span(file,row),value=byId.get(row.value?.['@id']);
   demand(range&&value,'Numeric edits require an existing literal source value');
   const text=Buffer.from(file.source).subarray(range.start,range.end).toString('utf8');
   const match=/=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*;$/.exec(text);
   demand(match&&value['sysx:sourceText']?.trim()===match[1],'Numeric edits currently support a single literal value expression');
   const start=range.start+Buffer.byteLength(text.slice(0,match.index+match[0].indexOf(match[1])));
   return{document:file.path,start,end:start+Buffer.byteLength(match[1]),oldText:match[1],newText:String(op.value)};
  }
  demand(/^[A-Za-z_][A-Za-z0-9_]*$/.test(row.declaredName),'Renaming quoted identifiers requires a qualified source adapter');
  const ranges=rows.filter(r=>r===row||Object.entries(r).some(([k,v])=>k!=='@id'&&references(v,row['@id']))).map(bounds).filter(Boolean);
  return{oldText:row.declaredName,newText:op.name,ranges};
 });
 const tokens=new Map();
 for(const e of edits){
  const op=operations[e.operationIndex],file=fileBy.get(e.document);
  demand(Number.isInteger(e.operationIndex)&&op&&file,'Unknown edit witness operation or document');
  demand(e.target===op.locator,'Edit witness target differs from the authorized operation');
  demand(Number.isInteger(e.offset)&&Number.isInteger(e.length)&&e.offset>=0&&e.length>=0&&validText(e.oldText)&&validText(e.newText),'Invalid edit witness span or text');
  const bytes=Buffer.from(file.source);demand(e.offset+e.length<=bytes.length&&bytes.subarray(e.offset,e.offset+e.length).equals(Buffer.from(e.oldText)),'Edit witness differs from accepted UTF-8 bytes');
  const allowed=permitted[e.operationIndex];
  demand(e.oldText===allowed.oldText&&e.newText===allowed.newText,'Source replacement is outside the authorized command');
  if(op.type==='set-value')demand(e.document===allowed.document&&e.offset===allowed.start&&e.offset+e.length===allowed.end,'Numeric edit is outside its authorized value expression');
  else{
   if(!tokens.has(e.document))tokens.set(e.document,identifiers(file.source));
   demand(tokens.get(e.document).some(t=>t.start===e.offset&&t.end===e.offset+e.length&&t.text===e.oldText)&&allowed.ranges.some(r=>r.document===e.document&&e.offset>=r.start&&e.offset+e.length<=r.end),'Rename is outside verified declaration/reference source tokens');
  }
 }
 for(let i=0;i<operations.length;i++){const count=edits.filter(e=>e.operationIndex===i).length;demand(operations[i].type==='set-value'?count===1:count>0,'Incomplete or additional operation witnesses');}
 return edits;
}
