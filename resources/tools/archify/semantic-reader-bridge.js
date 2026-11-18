(() => {
  'use strict';
  const config = JSON.parse(document.getElementById('model-bridge-data').textContent);
  let lastState = '', restoring = false, queued = false;
  const send = value => parent.postMessage({...value, channel: 'semantic-reader', view: config.view}, '*');
  const api = () => window.Archify;
  function publish() {
    queued = false;
    if (restoring || !api()) return;
    const a = api(), focus = a.focus?.active(), reach = a.focus?.reachability(), route = a.routeProbe?.result();
    const state = JSON.stringify({version:1, focus, relation:a.focus?.relationship()?.id || null,
      reach:reach?.direction || null, route:route ? {source:route.source,target:route.target,journey:route.journey} : null,
      lens:a.semanticLens?.active(), camera:a.view?.state(),
      collapsed:a.treeBranches?.collapsedIds?.() || []});
    if (state === lastState) return;
    lastState = state;
    send({type:'state', state, node:typeof focus === 'string' && !a.focus?.relationship() ? config.nodes[focus] || null : null});
  }
  function schedule() { if (!queued) {queued = true; queueMicrotask(publish);} }
  function validState(s){
    const known=id=>typeof id==='string'&&Object.hasOwn(config.nodes,id),list=(v,max,check)=>Array.isArray(v)&&v.length<=max&&v.every(check);
    return s&&s.version===1&&(s.focus==null||known(s.focus)||list(s.focus,1000,known))&&
      (s.relation==null||typeof s.relation==='string'&&config.relationships?.includes(s.relation))&&
      (s.reach==null||['upstream','downstream'].includes(s.reach))&&
      (s.route==null||s.route&&known(s.route.source)&&known(s.route.target)&&(s.route.journey==null||Number.isInteger(s.route.journey)&&s.route.journey>=0))&&
      (s.lens==null||list(s.lens,2,k=>typeof k==='string'))&&
      (s.collapsed==null||list(s.collapsed,1000,known))&&
      (s.camera==null||typeof s.camera==='object'&&typeof s.camera.scale==='number'&&s.camera.scale>0&&[s.camera.scale,s.camera.x,s.camera.y].every(Number.isFinite));
  }
  function restore(value, nodeId) {
    const a = api(); if (!a) return;
    restoring = true; let deferred = false;
    try {
      let saved;
      try {saved = typeof value === 'string' && value.startsWith('{') ? JSON.parse(value) : null;} catch (_) {return;}
      if(saved&&!validState(saved)){send({type:'restore-error',message:'Saved reading state is invalid for this view.'});return;}
      if (saved?.version === 1) {
        a.focus?.clear({updateUrl:false}); a.routeProbe?.clear({updateUrl:false}); a.semanticLens?.clear({updateUrl:false,preserveView:true});
        if (Array.isArray(saved.focus)) a.focus?.setMany(saved.focus.filter(id=>config.nodes[id]), {updateUrl:false});
        else if (config.nodes[saved.focus]) a.focus?.set(saved.focus,{updateUrl:false,toggle:false});
        if (saved.relation) a.focus?.inspectRelationshipById(saved.relation,{updateUrl:false,toggle:false});
        if (saved.reach) a.focus?.reach(saved.reach,{updateUrl:false,toggle:false,reveal:false});
        if (saved.route && config.nodes[saved.route.source] && config.nodes[saved.route.target]) {
          a.routeProbe?.begin({source:saved.route.source,focusNode:false});a.routeProbe?.choose(saved.route.target,{updateUrl:false});
          if (Number.isInteger(saved.route.journey)) a.routeProbe?.selectJourneyIndex(saved.route.journey);
        }
        for (const kind of (saved.lens || []).slice(0,2)) a.semanticLens?.select(kind);
        a.treeBranches?.restoreAll?.();
        for (const id of saved.collapsed || []) if (config.nodes[id]) a.treeBranches?.collapse?.(id);
        // Camera restores after semantic reveals have settled. Motion never resumes automatically.
        deferred = true;
        requestAnimationFrame(()=>{a.view?.restore(saved.camera);restoring=false;publish();});
        return;
      }
      if (typeof value === 'string' && value) {location.hash=value;}
      else if (nodeId && config.nodes[nodeId]) a.focus?.set(nodeId,{updateUrl:false,toggle:false});
    } finally {if (!deferred) restoring = false;}
    schedule();
  }
  document.addEventListener('click', event => {
    const relation = event.target.closest('[data-model-relation]');
    if (relation) send({type:'source',elementId:relation.dataset.modelRelation,label:relation.dataset.relationLabel});
    schedule();
  });
  for (const name of ['hashchange','pointerup','keyup','resize']) addEventListener(name,schedule);
  new MutationObserver(schedule).observe(document.querySelector('.diagram-container'),
    {subtree:true,attributes:true,attributeFilter:['data-focus-selected','aria-pressed','data-reach-active','data-route-active','data-lens-active','data-tree-collapsed','style']});
  addEventListener('message', event => {
    if (event.source !== parent || event.data?.channel !== 'semantic-reader-host') return;
    if (typeof event.data.linkTemplate === 'string') document.documentElement.setAttribute('data-reading-link-template',event.data.linkTemplate);
    restore(event.data.state,event.data.nodeId);
  });
  send({type:'ready'});
})();
