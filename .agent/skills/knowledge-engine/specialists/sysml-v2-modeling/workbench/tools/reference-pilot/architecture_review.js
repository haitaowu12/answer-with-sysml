(() => {
  'use strict';
  const D = JSON.parse(document.getElementById('reader-data').textContent);
  const A = D.architecture, R = D.records, V = Object.values(D.views);
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => Array.from(root.querySelectorAll(s));
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const label = id => R[id]?.label || id || 'Unspecified';
  const unique = a => Array.from(new Set(a));
  const list = name => A[name] || [];
  const button = (id, text) => R[id] || id==='reader:assurance' || String(id).startsWith('evidence:') ? `<button class="text-button" data-inspect="${esc(id)}">${esc(text || label(id))}</button>` : `<span>${esc(text || label(id))}</span>`;
  const excerpt = (s, n=125) => String(s || '').length > n ? String(s).slice(0,n).replace(/\s+\S*$/,'') + '…' : String(s || '');
  const pill = (text, cls='') => `<span class="pill ${esc(cls)}">${esc(text || 'proposed')}</span>`;
  const links = ids => unique(ids.filter(Boolean)).map(id => button(id)).join(' · ');
  const main = $('#main'), inspector = $('#inspector'), search = $('#global-search');
  const legacy = Object.fromEntries(D.evidence.map(r => [r.id, r]));
  const filters = {requirements:{q:'',kind:'all',page:1},evidence:{q:'',kind:'all',page:1}};
  const sections = ['overview','operational','functions','logical','scenarios','requirements','decisions','evidence'];
  const modes = {
    operational:[['activities','Roles & activities'],['boundary','Service boundary']],
    functions:[['flow','Functional exchanges'],['decomposition','Decomposition']],
    logical:[['interfaces','Service interfaces'],['allocation','Function allocation'],['decomposition','Responsibility breakdown']],
    scenarios:[['scenario','Scenario paths'],['states','Lifecycle states']],
    requirements:[['requirements','Requirements & planned checks'],['coverage','Source scope coverage'],['journeys','Journey continuity']],
    decisions:[['insights','Architecture insights'],['decisions','Open decisions'],['parameters','Unresolved quantities']],
  };
  const heading = {
    operational:['Operational analysis','Who does what, in which operating context?'],
    functions:['System functions','How responsibilities connect to deliver an outcome'],
    logical:['Logical architecture','Where functions sit, and which contracts cross boundaries'],
    scenarios:['Scenarios & states','Follow the conditions, exceptions and recovery obligations'],
    requirements:['Requirements & verification','Connect each criterion to a subject and a planned check'],
    decisions:['Decisions & insights','Use the architecture to decide what needs to change or be agreed'],
    evidence:['Source evidence','One searchable inventory, with the source available on demand'],
  };
  let current = {}, zoom = 1, natural = [900,500], activeGraph = null;
  let inspectorOpener = null;
  const featured = list('scenarios').find(s => s.id === A.reviewStart) || list('scenarios')[0];
  const functionRoots = list('functions').filter(f => !f.parent).map(f => f.id);
  function groupOf(id) {
    let seen = new Set();
    while (R[id]?.parent && !functionRoots.includes(R[id].parent) && !seen.has(id)) { seen.add(id); id=R[id].parent; }
    return id;
  }
  function preferredScope(section, mode) {
    const available = V.filter(v => v.section===section && v.mode===mode);
    if (section==='scenarios' && mode==='scenario' && featured) return featured.id;
    if (section==='functions' && featured) {
      const groups = featured.steps.map(s => groupOf(s.function));
      const preferred = groups.sort((a,b) => groups.filter(x=>x===b).length-groups.filter(x=>x===a).length)[0];
      if (available.some(v=>v.scope===preferred)) return preferred;
    }
    return available[0]?.scope || '';
  }
  function readState() {
    const raw = location.hash.slice(1), split = raw.indexOf('?');
    const section = split<0 ? raw : raw.slice(0,split), p = new URLSearchParams(split<0?'':raw.slice(split+1));
    const result = {section:sections.includes(section)?section:'overview', mode:p.get('mode'), scope:p.get('scope'), selected:p.get('selected')};
    result.mode ||= modes[result.section]?.[0]?.[0] || '';
    if (modes[result.section] && !modes[result.section].some(x=>x[0]===result.mode)) result.mode=modes[result.section][0][0];
    result.scope ||= preferredScope(result.section,result.mode);
    return result;
  }
  function navigate(section, values={}) {
    const p = new URLSearchParams();
    for (const [k,v] of Object.entries(values)) if (v) p.set(k,v);
    const hash = '#'+section+(p.size?'?'+p:'');
    if (location.hash===hash) render(); else location.hash=hash;
  }
  function setSelection(id, opener) {
    if (id && inspector.hidden) inspectorOpener = opener || document.activeElement;
    current.selected=id;
    const p = new URLSearchParams();
    for (const k of ['mode','scope','selected']) if (current[k]) p.set(k,current[k]);
    history.replaceState(null,'','#'+current.section+(p.size?'?'+p:''));
    showInspector(id);
    if (!id) {
      const target = inspectorOpener?.isConnected && !inspectorOpener.closest('[hidden]')
        ? inspectorOpener : search;
      inspectorOpener = null;
      target.focus();
    }
  }
  function modeButtons(section, selected) {
    return `<div class="mode-tabs" aria-label="Perspective">${(modes[section]||[]).filter(([m])=>!['operational','functions','logical','scenarios'].includes(section)||V.some(v=>v.section===section&&v.mode===m)).map(([m,l])=>`<button data-mode="${m}" class="${m===selected?'active':''}" aria-pressed="${m===selected}">${esc(l)}</button>`).join('')}</div>`;
  }
  function pageHeading(section) {
    const [title,sub]=heading[section];
    return `<div class="page-heading"><div><div class="eyebrow">${esc(A.scope?.phase?.split('.')[0] || 'Concept architecture for review')}</div><h1>${title}</h1><p>${sub}</p></div><span class="quiet-label">${esc(A.scope?.status || 'Proposed')}</span></div>`;
  }
  function sourceLink(ref, pages) {
    const page = pages?.[0] || String(ref).match(/PDF\s+(\d+)/)?.[1];
    return D.sourcePdf && page ? `<a class="source-ref" href="${D.sourcePdf}#page=${Number(page)}" target="_blank" rel="noopener">${esc(ref)} ↗</a>` : `<span class="source-ref">${esc(ref)}</span>`;
  }
  function overview() {
    const threads = unique(list('scenarios').map(s=>s.slice||s.id)).map(slice=>list('scenarios').find(s=>s.id===slice)||list('scenarios').find(s=>(s.slice||s.id)===slice));
    const leafs = list('functions').filter(f=>!list('functions').some(c=>c.parent===f.id));
    const priorities = list('insights').slice(0,3);
    main.innerHTML = `<div class="page"><div class="page-heading overview-heading"><div><div class="eyebrow">An architecture to question, inspect and refine</div><h1>${esc(A.scope?.name||A.title||'Connected system architecture')}</h1><p class="overview-intro">${esc(A.scope?.decision||'Review the responsibilities, exchanges and conditions that connect the intended outcomes.')}</p></div><span class="quiet-label">Concept / ${esc(A.scope?.status||'proposed')}</span></div>
      <div class="overview-summary"><section class="decision-panel"><div class="small-caps">Start with a connected case</div><h2>${esc(featured?.label||'Explore the model')}</h2><p>${esc(featured?.description||A.scope?.boundary||'')}</p><button class="primary" data-route="scenarios" data-scope="${esc(featured?.id||'')}" data-route-mode="scenario">Follow this scenario <span aria-hidden="true">→</span></button></section>
      <section class="priority-panel"><h2>What the architecture brings into focus</h2>${priorities.map((r,i)=>`<div class="priority-row"><span class="priority-number">0${i+1}</span>${button(r.id)}</div>`).join('')}<div class="priority-row"><button class="text-button" data-route="decisions">Explore ${list('insights').length} insights and ${list('decisions').length} decisions →</button></div></section></div>
      <div class="section-heading"><h2>Explore an operational thread</h2><p>${threads.length} connected slices · ${list('scenarios').length} nominal, exception and recovery cases</p></div>
      <div class="thread-grid">${threads.map((s,i)=>{const count=list('scenarios').filter(x=>(x.slice||x.id)===(s.slice||s.id)).length;return `<button class="thread-card" data-route="scenarios" data-route-mode="scenario" data-scope="${esc(s.id)}"><span>THREAD ${String(i+1).padStart(2,'0')}</span><strong>${esc(s.label)}</strong><small>${s.steps?.length||0} steps${count>1?' · '+count+' cases':''} <span aria-hidden="true">↗</span></small></button>`;}).join('')}</div>
      <div class="counts-strip"><span><strong>${leafs.length}</strong> leaf functions</span><span><strong>${list('exchanges').length}</strong> explicit exchanges</span><span><strong>${list('allocations').length}</strong> candidate allocations</span><span><strong>${list('requirements').length}</strong> requirements with planned review</span></div>
      <details class="scope-summary"><summary>Boundary, exclusions and validation basis</summary><p>${esc(A.scope?.boundary||'')}</p><div class="view-context"><div><h3>Included</h3><ul>${(A.scope?.included||[]).map(t=>'<li>'+esc(t)+'</li>').join('')}</ul></div><div><h3>Outside this study</h3><ul>${(A.scope?.excluded||[]).map(t=>'<li>'+esc(t)+'</li>').join('')}</ul></div></div><p>${esc(D.assurance.explanation)}</p><p>Verification cases are plans. No executed result or engineering acceptance is supplied.</p>${button('reader:assurance','Inspect the validation receipt')}</details></div>`;
  }
  function graphPage() {
    let available=V.filter(v=>v.section===current.section&&v.mode===current.mode);
    activeGraph=available.find(v=>v.scope===current.scope)||available[0];
    if (!activeGraph) {main.innerHTML=`<div class="page">${pageHeading(current.section)}<div class="empty-state">No explicit relationships are supplied for this perspective. Add and review the architecture records before a view can be projected.</div></div>`;return;}
    current.scope=activeGraph.scope;
    let selector='';
    if(current.section==='scenarios'&&current.mode==='scenario') {
      const selected=R[current.scope],slice=selected.slice||selected.id;
      const slices=unique(list('scenarios').map(s=>s.slice||s.id));
      selector=`<div class="field"><label for="slice-select">Operational thread</label><select id="slice-select" data-slice>${slices.map(id=>{const s=list('scenarios').find(s=>s.id===id)||list('scenarios').find(s=>(s.slice||s.id)===id);return `<option value="${esc(id)}" ${id===slice?'selected':''}>${esc(s.label)}</option>`;}).join('')}</select></div><div class="field"><label for="scope-select">Case</label><select id="scope-select" data-scope-select>${list('scenarios').filter(s=>(s.slice||s.id)===slice).map(s=>`<option value="${esc(s.id)}" ${s.id===current.scope?'selected':''}>${esc(s.kind||'case')} · ${esc(s.label)}</option>`).join('')}</select></div>`;
    } else if(available.length>1) selector=`<div class="field"><label for="scope-select">Selected scope</label><select id="scope-select" data-scope-select>${available.map(v=>`<option value="${esc(v.scope)}" ${v.scope===current.scope?'selected':''}>${esc(v.label)}</option>`).join('')}</select></div>`;
    const concurrent=R[current.scope]?.parallelGroups?.length;
    main.innerHTML=`<div class="page">${pageHeading(current.section)}<div class="view-controls">${modeButtons(current.section,current.mode)}${selector}</div><div class="purpose"><span class="q" aria-hidden="true">?</span><strong>${esc(activeGraph.question)}</strong></div>${concurrent?`<div class="concurrency-callout">This selected case requires both concurrent contributions before the join. ${button(current.scope,'Inspect entry conditions and excluded variants →')}</div>`:''}<div class="diagram-card"><div class="diagram-toolbar"><span class="diagram-stats">${activeGraph.nodeCount} displayed elements · ${activeGraph.relationCount} relationships</span><button data-zoom="fit">Fit all</button><button data-zoom="width">Fit width</button><button data-zoom="out" aria-label="Zoom out">−</button><span class="zoom-readout" id="zoom-readout">100%</span><button data-zoom="in" aria-label="Zoom in">+</button><a href="${esc(activeGraph.file)}" download>Export SVG ↓</a><a href="model.sysml" download>Native model ↓</a></div><div class="diagram-viewport" tabindex="0" aria-label="Architecture diagram. Tab to inspect elements. Use plus and minus to zoom."><div class="diagram-stage">${activeGraph.svg}</div></div><div class="diagram-note"><span>${esc(activeGraph.note)} Communication view; editable SysML is the native source.</span><span class="select-hint">Select a node or arrow to inspect ↗</span></div></div><div id="view-context"></div></div>`;
    const svg=$('.diagram-stage svg'),box=svg.getAttribute('viewBox').split(/[ ,]+/).map(Number);
    natural=[box[2],box[3]];
    requestAnimationFrame(()=>setZoom('initial'));
    renderContext();
  }
  function setZoom(action) {
    const viewport=$('.diagram-viewport'),svg=$('.diagram-stage svg'),stage=$('.diagram-stage');
    if(!viewport||!svg)return;
    const fitWidth=Math.max(.15,(viewport.clientWidth-30)/natural[0]),fitAll=Math.max(.12,Math.min(fitWidth,(viewport.clientHeight-20)/natural[1]));
    if(action==='fit')zoom=fitAll; else if(action==='width')zoom=Math.min(1.6,fitWidth); else if(action==='initial')zoom=fitAll>=.7?Math.min(1.2,fitAll):Math.min(1.15,fitWidth); else if(action==='in')zoom=Math.min(3.5,zoom*1.2); else if(action==='out')zoom=Math.max(.12,zoom/1.2);
    svg.style.width=(natural[0]*zoom)+'px';svg.style.height=(natural[1]*zoom)+'px';
    stage.style.width=Math.max(viewport.clientWidth,natural[0]*zoom+20)+'px';
    $('#zoom-readout').textContent=Math.round(zoom*100)+'%';
  }
  function renderContext() {
    const target=$('#view-context'),r=R[current.scope];if(!target||!r)return;
    const box=(title,body)=>`<section class="context-card"><h3>${title}</h3>${body}</section>`;
    let cards=[];
    if(current.mode==='scenario') {
      cards.push(box('Entry conditions','<ul>'+(r.entryConditions||[]).map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'));
      cards.push(box('Exit conditions','<ul>'+(r.exitConditions||[]).map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'));
      if(r.parallelGroups?.length)cards.push(box('Concurrent obligations','<ul>'+r.parallelGroups.map(p=>'<li>'+esc(p.description)+'</li>').join('')+'</ul>'));
      if(r.exceptions?.length)cards.push(box('Exception policy','<ul>'+r.exceptions.map(e=>'<li>'+esc(e.trigger)+' '+button(e.decisionId,'Inspect decision →')+'</li>').join('')+'</ul>'));
    } else if(current.mode==='states') {
      cards.push(box('Lifecycle subject','<p>'+button(r.subject)+'</p>'));
      cards.push(box('Lifecycle boundary','<p>'+esc(r.lifecycleExitCondition||((r.terminalStates||[]).length?'Declared terminal states: '+r.terminalStates.map(s=>R[r.id+'/'+s]?.label||s).join(', '):'No terminal condition is declared.'))+'</p>'));
    } else {
      const affected=list('decisions').filter(d=>(d.affects||[]).includes(current.scope)||(d.affects||[]).some(id=>R[id]?.parent===current.scope));
      cards.push(box('Selected responsibility','<p>'+esc(r.description||'')+'</p><p style="margin-top:8px">'+button(r.id,'Inspect context and source →')+'</p>'));
      if(affected.length)cards.push(box('Decisions that affect this slice','<p>'+affected.slice(0,4).map(d=>button(d.id)).join('<br>')+'</p>'));
    }
    target.innerHTML='<div class="view-context">'+cards.join('')+'</div>';
  }
  function requirementsPage() {
    const f=filters.requirements;
    main.innerHTML=`<div class="page">${pageHeading('requirements')}<div class="view-controls">${modeButtons('requirements',current.mode)}<div class="field"><label for="table-query">Find in this table</label><input type="search" id="table-query" data-table-query value="${esc(f.q)}" placeholder="Subject, criterion, source section…"></div></div><div class="purpose"><span class="q" aria-hidden="true">?</span><strong>${current.mode==='requirements'?'What must hold, for which subject, and what evidence is planned?':current.mode==='coverage'?'Where is each source scope represented or explicitly deferred?':'Where did each original journey go in the connected architecture?'}</strong></div><div id="table-content"></div><p class="muted" style="font-size:11px">Coverage is a disposition of scope. Planned checks are not executed results; neither establishes engineering acceptance.</p></div>`;
    updateTable();
  }
  function evidencePage() {
    const f=filters.evidence,types=unique(D.evidence.map(r=>r.kind)).sort();
    main.innerHTML=`<div class="page">${pageHeading('evidence')}<div class="evidence-source"><span class="source-icon" aria-hidden="true">▤</span><div><strong>${esc(A.source?.title||'Supplied source')}</strong><p>${esc(A.source?.versionNote||'')} ${esc(A.source?.pageConvention||'')}</p></div>${D.sourcePdf?`<a href="${D.sourcePdf}" target="_blank" rel="noopener">Open source PDF ↗</a>`:''}</div><div class="view-controls"><div class="field"><label for="table-query">Search ${D.evidence.length.toLocaleString()} retained source records</label><input type="search" id="table-query" data-table-query value="${esc(f.q)}" placeholder="Keyword, paragraph, identifier…"></div><div class="field"><label for="evidence-kind">Record kind</label><select id="evidence-kind" data-table-kind><option value="all">All kinds</option>${types.map(t=>`<option value="${esc(t)}" ${f.kind===t?'selected':''}>${esc(t)}</option>`).join('')}</select></div></div><div id="table-content"></div></div>`;
    updateTable();
  }
  function updateTable() {
    const f=filters[current.section],query=f.q.trim().toLowerCase();let rows,headers,renderRow;
    if(current.section==='evidence') {
      rows=D.evidence.filter(r=>f.kind==='all'||r.kind===f.kind);
      headers=['Source record','Kind / scope','Statement'];
      renderRow=r=>`<tr><td>${button('evidence:'+r.id,r.label||r.id)}<small>${esc(r.id)}</small></td><td>${esc(r.kind)}<small>§${esc(r.section||'—')} · PDF ${(r.pages||[]).map(esc).join(', ')}</small></td><td>${esc(excerpt(r.text,170))}</td></tr>`;
    } else if(current.mode==='requirements') {
      rows=list('requirements');headers=['Requirement','Subject','Obligation','Planned check'];
      renderRow=r=>{const checks=list('verificationCases').filter(v=>(v.requirementIds||[]).includes(r.id));return `<tr><td>${button(r.id)}<small>${esc(r.id)} · ${esc(r.basis||'derived')}</small></td><td>${button(r.subject)}</td><td>${esc(r.statement||r.criterion)}</td><td>${checks.length?checks.map(v=>button(v.id,v.method||v.label)+'<small>'+esc(v.status||'planned')+' · no execution supplied</small>').join(''):'No planned check supplied'}</td></tr>`;};
    } else if(current.mode==='coverage') {
      rows=A.coverage?.sourceSections||[];headers=['Source scope','Disposition','Architecture reference','Reason'];
      renderRow=r=>`<tr><td><strong>§${esc(r.sourceSection)}</strong><small>${esc(r.label)}</small></td><td>${esc(r.disposition||'Unspecified')}</td><td>${links(r.modelIds||[])||'No model reference'}</td><td>${esc(r.reason||r.explanation||'')}</td></tr>`;
    } else {
      rows=A.coverage?.oldJourneyIds||[];headers=['Original journey','Connected cases','Disposition'];
      renderRow=r=>`<tr><td>${esc(r.label||r.oldJourneyId)}<small>${esc(r.oldJourneyId)}</small></td><td>${links(r.modelIds||[])||'No mapped scenario'}</td><td>${esc(r.reason||'')}</td></tr>`;
    }
    const total=rows.length;
    rows=rows.filter(r=>!query||JSON.stringify(r).toLowerCase().includes(query));
    const size=current.section==='evidence'?25:12,pages=Math.max(1,Math.ceil(rows.length/size));f.page=Math.min(f.page,pages);
    const start=(f.page-1)*size,shown=rows.slice(start,start+size);
    $('#table-content').innerHTML=`<div class="table-summary"><span>${rows.length.toLocaleString()} of ${total.toLocaleString()} records${rows.length?' · showing '+(start+1)+'–'+(start+shown.length):''}</span><span>Page ${f.page} of ${pages} <button data-page="${f.page-1}" ${f.page<=1?'disabled':''}>Previous</button> <button data-page="${f.page+1}" ${f.page>=pages?'disabled':''}>Next</button></span></div>${shown.length?`<div class="table-wrap"><table class="data-table"><thead><tr>${headers.map(h=>'<th scope="col">'+h+'</th>').join('')}</tr></thead><tbody>${shown.map(renderRow).join('')}</tbody></table></div>`:'<div class="empty-state">No records match this search. Change the terms or kind filter.</div>'}`;
  }
  function decisionsPage() {
    const key=current.mode==='decisions'?'decisions':current.mode==='parameters'?'parameters':'insights';
    const records=list(key);
    main.innerHTML=`<div class="page">${pageHeading('decisions')}<div class="view-controls">${modeButtons('decisions',current.mode)}</div><div class="section-heading"><h2>${records.length} ${key==='parameters'?'quantities and design inputs':key==='decisions'?'open decisions':'architecture insights'}</h2><p>${key==='parameters'?'Unknown values remain unknown.':'Derived implications and candidate options for review.'}</p></div><div class="card-grid">${records.map(r=>`<article class="decision-card"><div class="eyebrow">${esc(r.id)} · ${esc(r.basis||'proposed')}</div><h2>${esc(r.label)}</h2><p>${esc(key==='insights'?r.observation:key==='decisions'?r.question:r.value==null?'Value not supplied. '+r.description:String(r.value)+' '+r.unit+'. '+r.description)}</p>${key==='insights'?'<p><strong>Review implication.</strong> '+esc(r.implication)+'</p>':''}${button(r.id,key==='insights'?'Inspect the supporting relationships →':key==='decisions'?'Inspect alternatives and affected model →':'Inspect the input and decision →')}</article>`).join('')}</div></div>`;
  }
  function relationSection(title, ids, explain) {
    ids=unique(ids.filter(id=>R[id]));if(!ids.length)return '';
    return `<section><h3>${title}</h3><ul class="relation-list">${ids.map(id=>`<li>${explain?'<small>'+esc(explain(R[id]))+'</small>':''}${button(id)}</li>`).join('')}</ul></section>`;
  }
  function showInspector(identity) {
    if(!identity){inspector.hidden=true;$('.app-shell').classList.remove('inspecting');$$('.architecture-svg .selected').forEach(e=>e.classList.remove('selected'));return;}
    if(identity==='reader:assurance'){showAssurance();return;}
    const isLegacy=identity.startsWith('evidence:'),r=isLegacy?legacy[identity.slice(9)]:R[identity];
    if(!r){showInspector(null);return;}
    inspector.hidden=false;$('.app-shell').classList.add('inspecting');inspector.scrollTop=0;
    const category=isLegacy?'Retained source record':r.category;
    let body=`<div class="inspector-header"><span class="small-caps">${esc(category)}</span><button data-close-inspector aria-label="Close inspector">×</button></div><h2 id="inspector-heading">${esc(r.label||r.id)}</h2><p class="record-id">${esc(r.id)}</p>${pill(r.status||'proposed',r.status==='planned'?'':'proposed')}${r.basis?' '+pill(r.basis):''}<p class="description">${esc(isLegacy?r.text:r.statement||r.description||r.observation||'')}</p>`;
    const fields=[];
    for(const [key,title] of [['condition','Applicability / guard'],['guard','Guard predicate'],['exitGuard','Conditional exit criterion'],['event','Triggering event'],['effect','Effect / obligation'],['outcome','Declared outcome'],['criterion','Required criterion'],['question','Decision question'],['implication','Review implication'],['rationale','Rationale'],['method','Planned method'],['setup','Planned setup'],['expectedResult','Planned expected result'],['derivation','Display derivation']]) if(r[key])fields.push(`<dt>${title}</dt><dd>${esc(typeof r[key]==='string'?r[key]:JSON.stringify(r[key]))}</dd>`);
    if(r.value!==undefined)fields.push('<dt>Parameter value</dt><dd>'+esc(r.value==null?'Not supplied':r.value+' '+(r.unit||''))+'</dd>');
    if(fields.length)body+='<section><h3>Meaning in this view</h3><dl>'+fields.join('')+'</dl></section>';
    const direct=[[r.displaySource?'displaySource':'source','From'],[r.displayTarget?'displayTarget':'target','To'],['subject','Subject'],['function','Function'],['component','Logical responsibility'],['performer','Performer'],['actor','Responsible role'],['parent','Part of'],['scenario','Scenario'],['lifecycle','Lifecycle'],['decisionId','Decision']].filter(([k])=>r[k]&&R[r[k]]);
    if(direct.length)body+='<section><h3>Connected context</h3><dl>'+direct.map(([k,t])=>'<dt>'+t+'</dt><dd>'+button(r[k])+'</dd>').join('')+'</dl></section>';
    for(const [key,title] of [['options','Candidate alternatives'],['entryConditions','Entry conditions'],['exitConditions','Exit conditions']]) if(r[key]?.length)body+='<section><h3>'+title+'</h3><ul>'+r[key].map(x=>'<li>'+esc(typeof x==='string'?x:JSON.stringify(x))+'</li>').join('')+'</ul></section>';
    if(!isLegacy){
      body+=relationSection('Related model records',[...(r.relatedIds||[]),...(r.affects||[]),...(r.realizes||[]),...(r.participants||[]),...(r.derivedFrom||[]),...(r.decisionIds||[]),...(r.parameterIds||[])]);
      body+=relationSection('Function allocations',list('allocations').filter(x=>x.function===r.id||x.component===r.id).map(x=>x.id),x=>label(x.function)+' → '+label(x.component));
      body+=relationSection('Exchanges',list('exchanges').filter(x=>x.source===r.id||x.target===r.id).map(x=>x.id),x=>label(x.source)+' → '+label(x.target));
      body+=relationSection('Requirements on this subject',list('requirements').filter(x=>x.subject===r.id).map(x=>x.id));
      body+=relationSection('Planned verification',list('verificationCases').filter(x=>(x.requirementIds||[]).includes(r.id)).map(x=>x.id),()=> 'Planned · no executed result supplied');
      body+=relationSection('Decision dependencies',list('decisions').filter(x=>(x.affects||[]).includes(r.id)).map(x=>x.id));
      body+=relationSection('Contributing system functions',list('functions').filter(x=>(x.realizes||[]).includes(r.id)).map(x=>x.id));
      body+=relationSection('Contained responsibilities',Object.values(R).filter(x=>x.parent===r.id).map(x=>x.id));
      if(r.collection==='scenarios')body+=relationSection('Scenario steps',(r.steps||[]).map(x=>r.id+'/'+x.id));
    }
    const sources=isLegacy?[`D01 · §${r.section||'—'} · PDF ${(r.pages||[]).join(', ')}`]:(r.sourceRefs||[]);
    body+='<section><h3>Source basis</h3>'+(sources.length?sources.map(s=>sourceLink(s,isLegacy?r.pages:undefined)).join(''):'<p>No source locator supplied for this record.</p>')+'</section>';
    if(r.native||r.nativeContext)body+=`<section><details><summary>${r.native?'Native model identity':'Native lifecycle context'}</summary><p class="native-note">${r.native?'Source-bound identity; language checks and engineering acceptance remain separate.':'This record is shown within the lifecycle. The binding below identifies its lifecycle occurrence.'}</p><code>${esc((r.native||r.nativeContext).qualifiedName)}</code><p><a href="model.sysml" download>Download editable SysML ↓</a></p></details></section>`;
    if(isLegacy&&r.q)body+='<section><details><summary>Previous study identity</summary><code>'+esc(r.q)+'</code><p class="native-note">This is the identity in the retained source study, not a new architecture allocation.</p></details></section>';
    inspector.innerHTML=body;
    $$('.architecture-svg [data-record-id]').forEach(e=>e.classList.toggle('selected',e.dataset.recordId===identity));
    $('#announcement').textContent='Inspecting '+(r.label||r.id);
  }
  function showAssurance() {
    inspector.hidden=false;$('.app-shell').classList.add('inspecting');inspector.scrollTop=0;
    const c=D.checks;
    inspector.innerHTML=`<div class="inspector-header"><span class="small-caps">Validation basis</span><button data-close-inspector aria-label="Close inspector">×</button></div><h2 id="inspector-heading">${D.assurance.nativeChecked?'Native structure checked':'Authored projection'}</h2><p class="description">${esc(D.assurance.explanation)}</p><section><h3>Separate review states</h3><dl><dt>Recipe and emitted model</dt><dd>Matched by exact model digest and canonical recipe digest.</dd><dt>Native language and relationships</dt><dd>${D.assurance.nativeChecked?'Matching managed-report and native-fact receipt supplied.':'No matching successful native receipt supplied.'}</dd><dt>Engineering readiness</dt><dd>${esc(c?.reviewReadiness||'Not assessed')}</dd><dt>Engineering acceptance</dt><dd>${esc(c?.engineeringAcceptance||'Not assessed')}</dd><dt>Verification execution</dt><dd>No executed verification result is supplied by this reader.</dd></dl></section>${c?`<section><h3>Recorded checker findings</h3><p>${Number(c.errorCount||0)} errors · ${Number(c.reviewItemCount||0)} review items</p><ul class="issues-list">${(c.issues||[]).slice(0,20).map(i=>'<li>'+esc(i.subject||'')+' — '+esc(i.message||i.code)+'</li>').join('')}</ul>${(c.issues||[]).length>20?'<p>Further findings are in the complete receipt.</p>':''}<a href="architecture-checks.json" download>Download complete receipt ↓</a></section>`:''}<section><h3>Editable package files</h3><p><a href="architecture.json" download>Download architecture recipe ↓</a></p><p><a href="bindings.json" download>Download identity bindings ↓</a></p></section><section><details><summary>Model revision</summary><code>${esc(D.modelSha256)}</code></details></section>`;
  }
  function render() {
    inspectorOpener = null;
    current=readState();activeGraph=null;
    $$('#navigation a').forEach(a=>{if(a.dataset.section===current.section)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    if(current.section==='overview')overview();
    else if(['operational','functions','logical','scenarios'].includes(current.section))graphPage();
    else if(current.section==='requirements')requirementsPage();
    else if(current.section==='decisions')decisionsPage();
    else evidencePage();
    showInspector(current.selected);
    document.title=(heading[current.section]?.[0]||'Overview')+' · '+(A.scope?.name||'Architecture review');
  }
  function searchRecords() {
    const q=search.value.trim().toLowerCase(),panel=$('#search-results');
    if(q.length<2){panel.hidden=true;search.setAttribute('aria-expanded','false');return;}
    let matches=Object.values(R).filter(r=>r.collection!=='projectionGroups'&&[r.id,r.label,r.description,r.question,r.item].join(' ').toLowerCase().includes(q)).slice(0,9).map(r=>({id:r.id,label:r.label,kind:r.category}));
    matches.push(...D.evidence.filter(r=>[r.id,r.label,r.text].join(' ').toLowerCase().includes(q)).slice(0,Math.max(3,12-matches.length)).map(r=>({id:'evidence:'+r.id,label:r.label,kind:'Source · '+r.id})));
    panel.innerHTML=matches.length?matches.map(r=>`<button data-inspect="${esc(r.id)}"><small>${esc(r.kind)}</small><strong>${esc(r.label||r.id)}</strong></button>`).join(''):'<div class="empty-search">No matching architecture or source record.</div>';
    panel.hidden=false;search.setAttribute('aria-expanded','true');
  }
  document.addEventListener('click',event=>{
    const inspect=event.target.closest('[data-inspect],[data-record-id]');
    if(inspect){event.preventDefault();setSelection(inspect.dataset.inspect||inspect.dataset.recordId,inspect);$('#search-results').hidden=true;search.setAttribute('aria-expanded','false');return;}
    if(event.target.closest('[data-close-inspector]')){setSelection(null);return;}
    const route=event.target.closest('[data-route]');if(route){navigate(route.dataset.route,{mode:route.dataset.routeMode,scope:route.dataset.scope});return;}
    const mode=event.target.closest('[data-mode]');if(mode){const valid=V.some(v=>v.section===current.section&&v.mode===mode.dataset.mode&&v.scope===current.scope);navigate(current.section,{mode:mode.dataset.mode,scope:valid?current.scope:preferredScope(current.section,mode.dataset.mode)});return;}
    const z=event.target.closest('[data-zoom]');if(z){setZoom(z.dataset.zoom);return;}
    const page=event.target.closest('[data-page]');if(page&&!page.disabled){filters[current.section].page=Number(page.dataset.page);updateTable();return;}
    if(event.target.closest('[data-assurance]')){setSelection('reader:assurance',event.target.closest('[data-assurance]'));return;}
    if(!event.target.closest('.search-wrap')){$('#search-results').hidden=true;search.setAttribute('aria-expanded','false');}
  });
  document.addEventListener('change',event=>{
    if(event.target.matches('[data-scope-select]'))navigate(current.section,{mode:current.mode,scope:event.target.value});
    if(event.target.matches('[data-slice]')){const s=list('scenarios').find(s=>s.id===event.target.value)||list('scenarios').find(s=>(s.slice||s.id)===event.target.value);navigate('scenarios',{mode:'scenario',scope:s.id});}
    if(event.target.matches('[data-table-kind]')){filters[current.section].kind=event.target.value;filters[current.section].page=1;updateTable();}
  });
  document.addEventListener('input',event=>{
    if(event.target===search)searchRecords();
    if(event.target.matches('[data-table-query]')){filters[current.section].q=event.target.value;filters[current.section].page=1;updateTable();}
  });
  document.addEventListener('keydown',event=>{
    const editing=/INPUT|TEXTAREA|SELECT/.test(event.target.tagName);
    if(event.key==='/'&&!editing){event.preventDefault();search.focus();}
    if(event.key==='Escape'){if(!$('#search-results').hidden){$('#search-results').hidden=true;search.setAttribute('aria-expanded','false');search.focus();}else if(!inspector.hidden)setSelection(null);}
    if(event.target===search&&event.key==='ArrowDown'){$('#search-results button')?.focus();event.preventDefault();}
    if(event.target===search&&event.key==='Enter'&&!$('#search-results').hidden){$('#search-results button')?.click();event.preventDefault();}
    if(event.target.closest('.search-results')&&['ArrowDown','ArrowUp'].includes(event.key)){const b=$$('#search-results button'),i=b.indexOf(event.target);b[(i+(event.key==='ArrowDown'?1:-1)+b.length)%b.length]?.focus();event.preventDefault();}
    const mark=event.target.closest?.('[data-record-id]');
    if(mark&&['Enter',' '].includes(event.key)){event.preventDefault();setSelection(mark.dataset.recordId);}
    if(event.target.closest('.diagram-viewport')&&!editing){if(['+','='].includes(event.key)){event.preventDefault();setZoom('in');}if(event.key==='-'){event.preventDefault();setZoom('out');}if(event.key==='0'){event.preventDefault();setZoom('fit');}}
  });
  document.addEventListener('wheel',event=>{if(event.ctrlKey&&event.target.closest('.diagram-viewport')){event.preventDefault();setZoom(event.deltaY<0?'in':'out');}},{passive:false});
  window.addEventListener('hashchange',render);
  $('#project-name').textContent=A.scope?.name||A.title||'Architecture study';
  $('#assurance').classList.toggle('checked',D.assurance.nativeChecked);
  $('#assurance').innerHTML=`<span class="status-dot" aria-hidden="true"></span><span>${esc(D.assurance.label)}</span><button data-assurance>Inspect validation basis</button>`;
  render();
})();
