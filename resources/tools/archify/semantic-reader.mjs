// Assemble existing semantic projections in the shared, locally adapted reader.
import fs from 'node:fs';
import { applyTemplate, renderCards } from './upstream/renderers/shared/utils.mjs';

const [input, output] = process.argv.slice(2);
const data = JSON.parse(fs.readFileSync(input, 'utf8'));
const template = fs.readFileSync(new URL('./upstream/assets/template.html', import.meta.url), 'utf8');
const safeJson = value => JSON.stringify(value).replaceAll('<', '\\u003c').replaceAll('>', '\\u003e').replaceAll('&', '\\u0026');
const directed = new Set(JSON.parse(fs.readFileSync(new URL('./reader-semantics.json',import.meta.url),'utf8')).directedRelationships);
const bridge = fs.readFileSync(new URL('./semantic-reader-bridge.js', import.meta.url), 'utf8');
for (const view of data.views) {
  if (['matrix','browser'].includes(view.presentation)) continue;
  // Bind service-generated native marks from typed records, never labels.
  const attrs = value => String(value).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
  view.svg = view.svg.replace(/<(?:g|path|line|polyline)\b[^>]*>/g, tag => {
    const node = view.nodes.find(n => tag.includes('data-node-id="' + n.readerId + '"'));
    if (node && !tag.includes('data-model-element=')) return tag.slice(0,-1) +
      ` data-model-element="${attrs(node.elementId)}" data-selection-key="${attrs(node.selectionKey)}" data-model-revision="${attrs(view.sourceSha256)}" data-appearance-id="${attrs(JSON.stringify([view.id,node.id]))}">`;
    const edge = view.edges.find(e => tag.includes('data-edge-id="' + e.id + '"'));
    if (edge && !tag.includes('data-edge-traversal=')) return tag.replace(/ data-edge-label="[^"]*"/,'').slice(0,-1) +
      ` data-edge-label="${attrs(edge.label)}" data-model-relation="${attrs(edge.elementId)}" data-relation-label="${attrs(edge.label)}" data-edge-kind="${attrs(edge.kind)}" data-edge-traversal="${directed.has(edge.kind)?'directed':'inspect'}">`;
    return tag;
  });
  for (const node of view.nodes) view.svg=view.svg.replace(new RegExp('(data-node-id="'+node.readerId+'"[^>]*data-node-kind=")[^"]*"'), '$1'+attrs(node.role)+'"');
  const hasDirected = view.edges.some(edge=>directed.has(edge.kind));
  const style = `<style>
    body{padding:.5rem!important;background:transparent!important}
    .container{max-width:none!important}.header{display:none!important}
    .toolbar{position:relative!important;inset:auto!important;justify-content:flex-end;margin:0 0 .5rem}
    .diagram-container{min-height:400px!important;margin:0!important;border-radius:12px}
    .diagram-container>svg{max-height:580px!important}
    :root{--semantic-analysis-fill:#e9f1fc;--semantic-definition-fill:#f2edfc;--semantic-usage-fill:#e7f4f3;--semantic-muted:#58727d}
    html[data-theme="dark"]{--semantic-analysis-fill:#21354a;--semantic-definition-fill:#352e49;--semantic-usage-fill:#183c3d;--semantic-muted:#b4ccd4}
    ${hasDirected ? '' : '#btn-route-probe{display:none!important}'}
    svg [data-model-relation]{cursor:pointer}
    @media(max-width:600px){.diagram-container{min-height:330px!important}.diagram-container>svg{max-height:430px!important;min-width:0!important;width:100%!important}}
  </style>`;
  const map = {view: view.id, nodes: Object.fromEntries(view.nodes.map(node => [node.readerId, node])),
    scopeElementId: view.projection.scopeElementId, relationships:view.edges.map(e=>e.id)};
  const host = `<script type="application/json" id="model-bridge-data">${safeJson(map)}</script><script>${bridge}</script>`;
  view.page = applyTemplate(template, {title: view.label, subtitle: '', svg: view.svg,
    cards: renderCards([]), locale: 'en', visualPreset: 'classic'})
    .replace('</head>', style + '</head>').replace('</body>', host + '</body>');
}
const shell = fs.readFileSync(new URL('./semantic-reader.html', import.meta.url), 'utf8');
fs.writeFileSync(output, shell.replace('<!-- MODEL_READER_DATA -->',
  `<script type="application/json" id="reader-data">${safeJson(data)}</script>`));
