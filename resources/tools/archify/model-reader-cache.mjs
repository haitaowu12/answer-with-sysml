/** Publish only reader artifacts derived from the currently accepted session. */
import {createHash} from 'node:crypto';
export function readerSnapshot(session){
 const project=structuredClone(session.project),snapshot=structuredClone(session.snapshot);
 return{project,snapshot,canUndo:session.canUndo,canRedo:session.canRedo,
  resolve(id){const entry=project.identities.find(i=>i.id===id),element=entry&&snapshot.elements.find(e=>e.locator===entry.locator);if(!element)throw Error('Unknown reader model identity');return {...element,id}}};
}
const keyOf=s=>createHash('sha256').update(JSON.stringify([s.project,s.canUndo,s.canRedo])).digest('hex');
export function createReaderCache(active,render){
 let cached;
 return{invalidate(){cached=undefined},async read(){
  for(;;){
   const session=active(),snapshot=readerSnapshot(session),key=keyOf(snapshot);
   if(cached?.session===session&&cached.key===key)return cached.page;
   const page=await render(snapshot);
   // A mutation or Open may finish while the renderer awaits native work.
   // Discard that obsolete artifact, including when revisions happen to match.
   if(active()!==session||keyOf(readerSnapshot(session))!==key)continue;
   cached={session,key,page};return page;
  }
 }};
}
