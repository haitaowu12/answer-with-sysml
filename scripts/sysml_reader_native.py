"""Typed semantic-to-native diagram mappings; geometry is presentation only."""
import copy
from html import escape
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

import archify

SVG = 'http://www.w3.org/2000/svg'
DIRECTED = {'containment', 'flow', 'transition', 'trace', 'TransitionUsage', 'FlowUsage', 'SuccessionFlowUsage', 'SuccessionAsUsage'}


def positions(nodes, edges):
    """Use Graphviz only to place fixed native cards, never to extract meaning."""
    ix = {n['id']: 'n' + str(i) for i, n in enumerate(nodes)}
    dot = ['digraph G {graph[rankdir=LR,nodesep=1.0,ranksep=1.9];node[shape=box,width=3,height=1.25,fixedsize=true,label=""];']
    dot += [value + ';' for value in ix.values()]
    dot += [ix[e['source']] + '->' + ix[e['target']] + ';' for e in edges]
    raw = subprocess.run(['dot', '-Tplain'], input='\n'.join(dot + ['}']), text=True,
                         capture_output=True, check=True, timeout=20).stdout
    rows = [line.split() for line in raw.splitlines()]
    height = float(next(r for r in rows if r[0] == 'graph')[3]) * 72
    coords = {r[1]: [round(float(r[2])*72 - 100 + 40, 2),
                     round(height - float(r[3])*72 - 40 + 40, 2)] for r in rows if r[0] == 'node'}
    return {key: coords[value] for key, value in ix.items()}


def native_spec(projection, nodes, edges, evidence):
    family = projection['viewKind']
    meta = {'title': projection['title'], 'animation': 'none', 'visual_preset': 'classic',
            'quality_profile': 'showcase', 'legend': {'mode': 'hidden'}}
    by_id = {n['id']: n for n in nodes}
    edge_rows = [dict(id=e['id'], **{'from': by_id[e['source']]['readerId'], 'to': by_id[e['target']]['readerId']}, label=e['label']) for e in edges]
    if family == 'decomposition':
        meta.pop('legend')
        parents = {e['target']: e['source'] for e in edges if e['kind'] == 'containment'}
        if len(parents) != len(edges):
            raise ValueError('Native Tree requires one ownership parent per node')
        items = []
        for n in nodes:
            item = {'id': n['readerId'], 'label': n['label'],
                    'sublabel': evidence[n['elementId']].get('type', '')}
            if n.get('referenced'): item['sublabel'] = 'Reference · ' + item['sublabel']
            if n['id'] in parents: item['parent'] = by_id[parents[n['id']]]['readerId']
            items.append(item)
        return {'schema_version': 1, 'diagram_type': 'tree', 'meta': meta,
                'layout': {'direction': 'down', 'nodeW': 160, 'nodeMaxW': 220, 'gapX': 32, 'gapY': 64}, 'nodes': items}, set()
    if family in ('states', 'actions'):
        b = projection.get('behavior')
        if not b or family != 'states':
            raise ValueError('This native mapping supports flat state transitions; action-control rendering needs its own profile')
        root = next(n for n in nodes if n['id'] == b['rootId'])
        states = [n for n in nodes if n['id'] != root['id']]
        if (root.get('parallel') is not False or any(n['parent'] != root['id'] or n.get('parallel') is True for n in states)
                or any(e['source'] == root['id'] or e['target'] == root['id'] for e in edges)):
            raise ValueError('Nested or concurrent states require the custom region renderer; no flattening is allowed')
        # Find a real transition path for the layout spine. All states stay
        # neutral; layout order does not invent an initial state or happy path.
        paths = []
        def visit(path):
            paths.append(path)
            if len(paths) > 10000: raise ValueError('State graph needs a custom region layout')
            for e in edges:
                if e['source'] == path[-1] and e['target'] not in path: visit(path + [e['target']])
        if len(states) > 16: raise ValueError('Select a smaller state scope')
        for n in sorted(states, key=lambda n: evidence[n['elementId']].get('line') or 0): visit([n['id']])
        spine = max(paths, key=len)
        if len(spine) < 2: raise ValueError('Native Lifecycle requires a connected transition path')
        meta['legend'] = {'mode': 'hidden'}
        transitions = []
        for i, (e, rel) in enumerate(zip(edges, b['relations']), 1):
            event = ' / '.join(q['text'] for q in rel['triggers'])
            label = f'R{i}' + (' · ' + event if event else ' · transition')
            item = {**edge_rows[i-1], 'label': label, 'variant': 'default'}
            if rel['guards'] or rel['effects']: item['note'] = 'Conditions / effects in R' + str(i)
            transitions.append(item)
        return {'schema_version': 3, 'diagram_type': 'lifecycle', 'meta': meta,
                'mainPath': [by_id[eid]['readerId'] for eid in spine],
                'states': [{'id': n['readerId'], 'type': 'neutral', 'label': n['label'], 'icon': 'none'} for n in states],
                'transitions': transitions}, {root['readerId']}
    if family == 'exchanges':
        if any(e['kind'] != 'flow' for e in edges): raise ValueError('Dataflow requires explicit flows only')
        incoming = {n['id']: 0 for n in nodes}
        for e in edges: incoming[e['target']] += 1
        ranks = {n['id']: 0 for n in nodes if incoming[n['id']] == 0}
        pending = set(by_id) - set(ranks)
        while pending:
            ready = [eid for eid in pending if all(e['source'] in ranks for e in edges if e['target'] == eid)]
            if not ready: raise ValueError('Cyclic transfers require a custom dataflow layout')
            for eid in ready:
                ranks[eid] = max((ranks[e['source']] + 1 for e in edges if e['target'] == eid), default=0)
                pending.remove(eid)
        count = max(ranks.values()) + 1
        if not 2 <= count <= 5: raise ValueError('Native Dataflow supports two to five transfer columns')
        row = {}; items = []
        for n in nodes:
            stage = ranks[n['id']]; at = row.get(stage, 0); row[stage] = at + 1
            parts = n['label'].split('\n')
            items.append({'id': n['readerId'], 'type': 'backend', 'label': parts[0],
                          'sublabel': ' · '.join(parts[1:]), 'icon': 'none', 'stage': stage, 'row': at})
        return {'schema_version': 1, 'diagram_type': 'dataflow', 'meta': meta,
                'stages': [{'label': 'Transfer origin' if i == 0 else 'Transfer destination' if i == count-1 else 'Intermediate component'} for i in range(count)],
                'nodes': items, 'flows': edge_rows}, set()
    coords = positions(nodes, edges)
    items = []
    for n in nodes:
        parts = n['label'].split('\n')
        kind = ('security' if n['role'] == 'requirement' else 'cloud' if n['role'] == 'check'
                else 'external' if n.get('referenced') else 'frontend' if evidence[n['elementId']]['kind'] == 'ReferenceUsage' else 'backend')
        sublabel = ' · '.join(parts[1:])
        if family in ('requirement', 'verification') and n['role'] == 'component':
            sublabel = 'Subject reference' if evidence[n['elementId']]['kind'] == 'ReferenceUsage' else 'Modeled component'
        items.append({'id': n['readerId'], 'type': kind, 'label': parts[0], 'sublabel': sublabel,
                      'icon': 'none', 'pos': coords[n['id']], 'size': [210, 90]})
    for e, item in zip(edges, edge_rows):
        item['variant'] = 'dashed' if e['kind'] in ('trace', 'binding') else 'emphasis' if e['kind'] == 'flow' else 'default'
    return {'schema_version': 1, 'diagram_type': 'architecture', 'meta': meta,
            'components': items, 'connections': edge_rows}, set()


def render_native(projection, nodes, edges, evidence):
    spec, scope_only = native_spec(projection, nodes, edges, evidence)
    with tempfile.TemporaryDirectory(prefix='semantic-native-') as temp:
        path = Path(temp) / 'view.json'; path.write_text(json.dumps(spec))
        html = Path(temp) / 'view.html'
        receipt = archify.render(path, html)
        raw = html.read_text()
        svg = ET.fromstring(re.search(r'<svg\b[^>]*role="img"[\s\S]*?</svg>', raw).group())
    # Lifecycle treats the first layout-spine node as initial unconditionally.
    # A layout spine is not an initial-state declaration in SysML.
    if spec['diagram_type'] == 'lifecycle':
        for parent in svg.iter():
            for child in list(parent):
                if 'data-lifecycle-initial-marker' in child.attrib or 'data-lifecycle-final-marker' in child.attrib:
                    parent.remove(child)
    by_reader = {n['readerId']: n for n in nodes}
    edge_map = {e['id']: e for e in edges}
    by_id = {n['id']: n for n in nodes}
    tree_edges = {(by_id[e['source']]['readerId'], by_id[e['target']]['readerId']):e for e in edges} if spec['diagram_type']=='tree' else {}
    seen_nodes, seen_edges = set(), set()
    for el in svg.iter():
        node = by_reader.get(el.get('data-node-id'))
        if node:
            seen_nodes.add(node['readerId']);el.set('data-model-element', node['elementId']);el.set('data-selection-key', node['selectionKey'])
        edge = tree_edges.get((el.get('data-edge-from'), el.get('data-edge-to'))) if tree_edges else edge_map.get(el.get('data-edge-id'))
        if edge:
            seen_edges.add(edge['id']);el.set('data-edge-id',edge['id']);el.set('data-model-relation', edge['elementId']);el.set('data-relation-label', edge['label'])
            if edge['kind'] not in DIRECTED:
                # The native architecture renderer has only arrowed links.
                # This explicit semantic-presentation adaptation removes the
                # arrow for typed contacts; the shared binding retains inspectable topology.
                for part in el.iter():
                    part.attrib.pop('marker-end', None);part.attrib.pop('marker-start', None)
                    part.attrib.pop('data-animate', None)
    from sysml_reader_binding import bind
    bind(svg,nodes,edges,view_id=projection.get('id',projection['viewKind']),revision=projection.get('sourceSha256',''))
    if seen_nodes != set(by_reader) - scope_only:
        raise ValueError('Native reader node marks differ from the selected semantic facts')
    # Every relationship is bound by exact ID or native containment endpoints.
    if seen_edges != set(edge_map):
        raise ValueError('Native reader relationship marks differ from semantic facts')
    return ET.tostring(svg, encoding='unicode'), spec, {'nativeChecks': receipt['automatedChecks'],
                'scopeOnlyNodes': sorted(scope_only), 'lifecycleInitialMarkerRemoved': spec['diagram_type'] == 'lifecycle', 'lifecycleFinalMarkerRemoved': spec['diagram_type'] == 'lifecycle', 'semanticDirectionAdaptation': any(e['kind'] not in DIRECTED for e in edges)}
