"""Custom presentations for qualified semantics without a faithful native match."""
import copy
import hashlib
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
Q = '{' + SVG + '}'
XLINK = '{http://www.w3.org/1999/xlink}'


def port_diagram(report, target, projection, nodes, edges, evidence):
    """Reuse the specialist's endpoint resolution and geometry; restyle its marks.

    Geometry never supplies identities or relationship meaning. Every mark is
    joined through the producer's typed presentation ID and endpoint witnesses.
    """
    import engineering
    detailed = engineering.interconnection(report, target)
    root = ET.fromstring(detailed['svg'])
    root.attrib.pop('width', None); root.attrib.pop('height', None)
    root.set('role', 'img'); root.set('aria-label', projection['question'])
    root.set('data-diagram-type', 'sysml-ports')
    # Plain background and the producer's working-level footer are presentation
    # chrome. Their evidence remains in the export, outside the reading flow.
    for child in list(root):
        if child.tag in (Q+'rect', Q+'text'): root.remove(child)
    marks = {m['presentationId']: m for m in detailed['marks']}
    model = {e['sessionElementId']: e for e in report['elements']}
    context_parts = {m['usageContext']: m['elementId'] for m in detailed['marks']
                     if m['elementId'] in detailed['partBounds']}
    by_element = {n['elementId']: n for n in nodes}
    extra = []; port_readers = {}
    connectors = {c['elementId']: c for c in detailed['connectors']}
    flows = {f['elementId'] for f in detailed['flows']}
    observed = set()
    for anchor in list(root):
        mark = marks.get(anchor.get('data-presentation-id'))
        if not mark: raise ValueError('Port layout contains an unbound mark')
        eid = mark['elementId']; semantic = model[eid]; kind = semantic['metaclass']
        anchor.tag = Q+'g'; anchor.attrib.clear()
        for title in anchor.findall(Q+'title'): anchor.remove(title)
        for child in list(anchor):
            if child.get('data-component-kind'): anchor.remove(child)
        if kind in ('PartDefinition', 'PartUsage', 'PortUsage'):
            if kind == 'PortUsage':
                pid = context_parts.get(mark['usageContext'])
                occurrence = projection['scopeElementId'] + '/' + ((pid + '/') if pid else '') + eid
                node = {'id': occurrence, 'elementId': eid, 'role': 'port',
                        'label': evidence[eid]['name'], 'selectionKey': 'occurrence:'+occurrence,
                        'readerId': 'm'+hashlib.sha256(occurrence.encode()).hexdigest()[:24]}
                extra.append(node);port_readers[(pid,eid)]=node['readerId']
            else:
                node = by_element.get(eid)
                if not node: raise ValueError('Visible port component is outside the qualified projection')
            anchor.attrib.update({'data-node-id':node['readerId'], 'data-node-label':node['label'].replace('\n',' · '),
                'data-model-element':eid, 'data-selection-key':node['selectionKey'], 'tabindex':'0',
                'role':'button','aria-label':'Select '+node['label'].replace('\n',' · '),'aria-pressed':'false'})
            for shape in anchor.findall(Q+'rect'):
                boundary = eid == projection['scopeElementId']
                shape.set('rx', '3' if kind == 'PortUsage' else '12')
                shape.set('fill', 'var(--bg)' if boundary else 'var(--node-backend-fill, #e9f5f5)')
                shape.set('stroke', 'var(--arrow)'); shape.set('stroke-width','1.5')
                if boundary: shape.set('stroke-dasharray','6 5')
            for path in anchor.findall(Q+'path'): anchor.remove(path)
        else:
            if eid not in connectors and eid not in flows:
                # Collections remain source-linked facts rather than fake parts.
                if not any(c['elementId']==eid for c in detailed['collections']):
                    raise ValueError('Unmapped custom relationship mark')
            anchor.set('data-model-relation',eid)
            anchor.set('data-relation-label', evidence[eid]['name'])
            candidates=[edge for edge in edges if edge['elementId']==eid]
            if eid in flows:
                contextual=[flow for flow in detailed['flows'] if flow['elementId']==eid and
                    mark['usageContext']==target+'/'+model[flow['connectionId']]['name']]
                if len(contextual)!=1:raise ValueError('Ambiguous flow usage context')
                flow=contextual[0]
                anchor.set('data-reader-endpoint-from',port_readers[tuple(flow['source'])]);anchor.set('data-reader-endpoint-to',port_readers[tuple(flow['target'])])
                candidates=[edge for edge in candidates if edge['source']==flow['source'][0] and edge['target']==flow['target'][0]]
            if eid in connectors:
                ends=connectors[eid]['endpoints']
                if len(ends)==2:
                    anchor.set('data-reader-endpoint-from',port_readers[tuple(ends[0])]);anchor.set('data-reader-endpoint-to',port_readers[tuple(ends[1])])
            if len(candidates)==1:anchor.set('data-edge-id',candidates[0]['id'])
            elif candidates:raise ValueError('Ambiguous custom relationship context')
            observed.add(eid)
        for element in anchor.iter():
            if element.tag == Q+'text':
                element.set('fill','var(--text)');element.set('stroke','var(--bg)')
                element.set('font-family','Inter,system-ui,sans-serif')
                if element.text == '«flow»': element.text = 'Transfer'
                if element.get('data-component-label'):
                    element.set('font-size','17');element.set('font-weight','600')
            elif element.tag in (Q+'path', Q+'polygon'):
                if element.get('stroke'):element.set('stroke','var(--arrow)')
                if element.get('fill') not in (None,'none'):element.set('fill','var(--arrow)')
                if eid in connectors and connectors[eid]['kind']=='BindingConnectorAsUsage':
                    element.set('stroke-dasharray','6 4')
    required = {e['elementId'] for e in edges}
    if not required <= observed:
        raise ValueError('Custom port diagram omits qualified relationships')
    nodes.extend(extra)
    from sysml_reader_binding import bind
    bind(root,nodes,edges,view_id=projection.get('id',projection['viewKind']),revision=projection.get('sourceSha256',''))
    # Exact endpoint witnesses, exclusions and geometry stay inspectable in the
    # sidecar. No generic renderer check is claimed for this custom presentation.
    detailed.pop('svg')
    return ET.tostring(root,encoding='unicode'), {'diagram_type':'custom-ports', **detailed}, {
        'semanticChecks': {'representedRelationships':len(required),'ports':len(extra),
                           'endpointProfile':detailed['notationProfile']}, 'browserReview':'pending'}


def matrix_view(base):
    """A GridView presentation over the same qualified interface projection."""
    view = copy.deepcopy(base)
    view.update(id=base['id']+'-matrix', label=base['scope']+' · Interface matrix',
                family='interface-matrix', presentation='matrix', derivedFrom=base['id'],
                question='Which components are connected, and what moves between them?')
    # Port occurrences remain in the port view; matrix axes are components.
    view['nodes'] = [n for n in view['nodes'] if n['role'] != 'port']
    axes = {n['id'] for n in view['nodes']}
    cells = {}
    for edge in view['edges']:
        if edge['source'] not in axes or edge['target'] not in axes:
            raise ValueError('Matrix relationship has an unresolved component axis')
        pairs = [(edge['source'],edge['target'])]
        if edge['kind'] not in ('flow','transition','trace') and edge['source'] != edge['target']:
            pairs.append((edge['target'],edge['source']))
        for pair in pairs: cells.setdefault(pair,[]).append(edge['id'])
    view['matrix'] = [{'row':r,'column':c,'relations':ids} for (r,c),ids in cells.items()]
    view['nativeDiagram'] = {'diagram_type':'custom-matrix'}
    view['renderChecks'] = {'semanticChecks':{'relationships':len(view['edges']),'cells':len(cells)},'browserReview':'pending'}
    view.pop('svg')
    return view
