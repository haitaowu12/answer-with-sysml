"""One correspondence contract for native and custom semantic reader marks.

Topology is inspectable for every binary relation. Directed path tools traverse
only explicit transfers/control transitions, never ownership, typing or contact.
"""
import json

import archify

DIRECTED = set(json.loads((archify.PACKAGE / 'reader-semantics.json').read_text())['directedRelationships'])


def bind(root, nodes, edges, *, view_id='view', revision=''):
    by_id = {node['id']: node for node in nodes}
    by_reader = {node['readerId']: node for node in nodes}
    by_relation = {}
    for edge in edges:
        by_relation.setdefault(edge['elementId'], []).append(edge)
    for mark in root.iter():
        node = by_reader.get(mark.get('data-node-id'))
        if node:
            if any(mark.get(key) not in (None, expected) for key, expected in (('data-model-element', node['elementId']), ('data-selection-key', node['selectionKey']))):
                raise ValueError('Contradictory node model correspondence')
            mark.attrib.update({'data-node-kind': node.get('role') or node.get('metaclass') or 'element',
                'data-model-element': node['elementId'], 'data-selection-key': node['selectionKey'],
                'data-appearance-id': json.dumps([view_id, node['id']], separators=(',', ':')),
                'data-model-revision': revision})
        candidates = by_relation.get(mark.get('data-model-relation'), [])
        if not candidates:
            continue
        # Prefer the exact projection edge identity where one source relation
        # has multiple contextual appearances. Never collapse by display name.
        edge = next((e for e in candidates if e['id'] == mark.get('data-edge-id')), None)
        if edge is None:
            if mark.get('data-edge-id') or len(candidates) != 1:
                raise ValueError('Ambiguous relationship appearance binding')
            edge = candidates[0]
        source, target = by_id[edge['source']], by_id[edge['target']]
        for key in ('data-reader-endpoint-from', 'data-reader-endpoint-to'):
            if mark.get(key) and mark.get(key) not in by_reader:
                raise ValueError('Reader endpoint has no contextual model correspondence')
        mark.attrib.update({'data-edge-from': mark.get('data-reader-endpoint-from',source['readerId']), 'data-edge-to': mark.get('data-reader-endpoint-to',target['readerId']),
            'data-edge-id': edge['id'], 'data-edge-key': json.dumps([view_id, edge['id']], separators=(',', ':')),
            'data-edge-label': edge['label'], 'data-edge-kind': edge['kind'],
            'data-edge-traversal': 'directed' if edge['kind'] in DIRECTED else 'inspect',
            'data-model-revision': revision})
    return root
