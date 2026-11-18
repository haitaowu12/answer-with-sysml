#!/usr/bin/env python3
"""Export existing qualified semantic viewpoints into one standalone reader.

The specialist extracts meaning and lays out its projections. This adapter only
adds native reader hooks, a common selector and source inspection.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'resources/tools/archify'
SPECIALIST = ROOT / '.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/tools/reference-pilot'
SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG)


def specialist():
    # Reuse the exact modules used by the existing reference lab. No new SysML
    # parser, semantic normalizer or alternate model is introduced here.
    if str(SPECIALIST) not in sys.path:
        sys.path.insert(0, str(SPECIALIST))
    import report_integrity
    import stakeholder
    import presentation
    return report_integrity, stakeholder, presentation


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def graph_facts(projection: dict) -> tuple[list, list]:
    """Translate typed projection fields, never SVG labels, into reader identity."""
    if 'behavior' in projection:
        b = projection['behavior']
        nodes = [dict(n, label=n['name'], elementId=n['elementId'], role=n['kind']) for n in b['nodes']]
        edges = [dict(e, label='R' + str(i), id='r' + str(i), kind=e['kind'])
                 for i, e in enumerate(b['relations'], 1)]
    else:
        nodes = [dict(n, elementId=n.get('elementId', n['id'])) for n in projection['nodes']]
        edges = [dict(e, id='r' + str(i)) for i, e in enumerate(projection['edges'], 1)]
    ids = [n['id'] for n in nodes]
    if not nodes or len(set(ids)) != len(ids):
        raise ValueError('Semantic view has missing or duplicate node identities')
    for edge in edges:
        if edge['source'] not in ids or edge['target'] not in ids:
            raise ValueError('Semantic view has an unresolved visible endpoint')
    for i, node in enumerate(nodes):
        node['readerId'] = 'm' + digest(node['id'].encode())[:24]
        node['layoutId'] = 'n' + str(i)
        # A decomposition's explicit occurrence path is also reconstructed for
        # immediate components in an interface view of that same definition.
        if node.get('selectionKey'):
            continue
        if node['id'] != node['elementId']:
            node['selectionKey'] = 'occurrence:' + node['id']
        elif projection['viewKind'] in ('connections', 'context', 'exchanges') and node['role'] == 'component':
            node['selectionKey'] = 'occurrence:' + projection['scopeElementId'] + '/' + node['id']
        else:
            node['selectionKey'] = 'element:' + node['elementId']
    return nodes, edges


def project_views(report: dict, requests: list, source: str, source_name: str, *, labels=None) -> dict:
    integrity, stakeholder, presentation = specialist()
    from behavior import label_map
    labels = label_map(labels)
    if report.get('reportIntegrity', {}).get('status') != 'verified-managed' or not report.get('staticChecksPassed'):
        raise ValueError('A qualified managed report is required')
    realized = {v['id']: v for v in report['views']}
    if not requests or len({v['id'] for v in requests}) != len(requests):
        raise ValueError('Reader requires uniquely named view recipes')
    source_lines = source.splitlines()
    evidence = {}
    for e in report['elements']:
        start, end = e.get('line'), e.get('endLine')
        if type(start) is int and 1 <= start <= len(source_lines):
            end = end if type(end) is int and start <= end <= len(source_lines) else start
            excerpt = '\n'.join(source_lines[start - 1:end])
        else:
            start, end, excerpt = None, None, 'Source location unavailable for this model element.'
        evidence[e['sessionElementId']] = {'name': presentation.display_name(e), 'kind': e['metaclass'],
            'type': ', '.join(stakeholder.types(e)),
            'line': start, 'endLine': end, 'excerpt': excerpt, 'file': source_name}
    views = []
    for request in requests:
        realized_view = realized.get(request['id'])
        if not realized_view or realized_view.get('viewRecipeSha256') != integrity.view_recipe_sha256(request):
            raise ValueError('View recipe differs from the qualified model report: ' + request['id'])
        # Labels are presentation data. Verify the original qualified recipe
        # before combining global labels with a view's more specific labels.
        request = dict(request, labels={**labels, **label_map(request.get('labels'))})
        targets = request.get('names', request.get('targets'))
        if not isinstance(targets, list) or len(targets) != 1:
            raise ValueError('Select one qualified target per reader view')
        if request.get('readerProfile'):
            from sysml_reader_profiles import project as semantic_project, STANDARD
            projection = semantic_project(report, request)
            nodes, edges = graph_facts(projection)
            if any(n['elementId'] not in evidence for n in nodes) or any(e['elementId'] not in evidence for e in edges):
                raise ValueError('A semantic view lacks source evidence')
            mode = projection['presentation']
            view = {'id':request['id'], 'label':projection['title'], 'question':projection['question'],
                    'scope':projection['scopeLabel'], 'family':projection['viewKind'], 'sourceSha256':report['sourceSha256'],
                    'projection':projection, 'nodes':nodes, 'edges':edges, 'readingRows':projection['rows'],
                    'standardView':STANDARD[request['readerProfile']],
                    'nativeDiagram':{'diagram_type':'custom-'+request['readerProfile']},
                    'renderChecks':{'semanticNodes':len(nodes),'semanticRelations':len(edges),'browserReview':'pending'}}
            if mode in ('browser','matrix'):
                view['presentation']=mode
                if mode=='matrix':
                    view['rowIds']=projection['details']['rowIds']; view['columnIds']=projection['details']['columnIds']
                    view['matrixCaption']=projection['details']['matrixCaption']
                    cells={}
                    for edge in edges:cells.setdefault((edge['source'],edge['target']),[]).append(edge['id'])
                    view['matrix']=[{'row':r,'column':c,'relations':ids} for (r,c),ids in cells.items()]
            else:
                from sysml_reader_diagrams import render as render_semantic
                view['svg']=render_semantic(projection,nodes,edges)
            view['readingLegend']=projection['details'].get('legend',[])
            view['readingNote']=projection['details'].get('scopeNote','')
            views.append(view)
            continue
        projection = stakeholder.project(report, targets[0], request)
        if projection['sourceSha256'] != report['sourceSha256']:
            raise ValueError('Projection changed its source revision')
        nodes, edges = graph_facts(projection)
        if any(n['elementId'] not in evidence for n in nodes) or any(e['elementId'] not in evidence for e in edges):
            raise ValueError('A view mark has no model evidence')
        from sysml_reader_native import render_native
        # A self-contained usage overview has no visible scope-boundary node.
        # Keep the producer's exact graph instead of importing the port layout's
        # enclosing frame as an extra component or interface-matrix axis.
        connection_overview = (projection['viewKind'] == 'connections' and
                               not any(n['elementId'] == projection['scopeElementId'] for n in nodes))
        if projection['viewKind'] == 'connections' and not connection_overview:
            from sysml_reader_custom import port_diagram
            svg, native, checks = port_diagram(report, targets[0], projection, nodes, edges, evidence)
        else:
            svg, native, checks = render_native(projection, nodes, edges, evidence)
        family = 'context' if connection_overview else projection['viewKind']
        labels = {'context': 'Overview', 'decomposition': 'Structure', 'connections': projection['scopeLabel'] + ' · Interfaces',
                  'states': projection['scopeLabel'] + ' · Behavior', 'actions': projection['scopeLabel'] + ' · Behavior',
                  'requirement': projection['scopeLabel'] + ' · Requirement',
                  'verification': projection['scopeLabel'] + ' · Verification', 'exchanges': 'Exchanges'}
        reading_rows = projection['rows']
        if 'behavior' in projection:
            reading_rows = []
            b = projection['behavior']; by_id = {n['id']: n for n in nodes}
            for i, relation in enumerate(b['relations'], 1):
                clauses = []
                for field, label in [('triggers','Trigger'),('guards','Guard'),('effects','Effect')]:
                    items = relation[field]
                    if items:
                        clauses.extend(label + ': ' + item['text'] + (' [excerpt truncated; inspect source]' if item.get('textTruncated') else '') for item in items)
                    elif relation.get('conditionStatus', {}).get(field) in ('unknown','unavailable'):
                        clauses.append(label + ': not supplied')
                reading_rows.append({'title':f'R{i}: ' + by_id[relation['source']]['label'] + ' → ' + by_id[relation['target']]['label'],
                    'body':' · '.join(clauses) or 'No explicit condition supplied.', 'elementIds':[relation['elementId']]})
        views.append({'id': request['id'], 'label': request.get('label') or labels[family],
                      'question': projection['question'], 'scope': projection['scopeLabel'], 'family': family,
                      'sourceSha256': report['sourceSha256'], 'projection': projection,
                      'nodes': nodes, 'edges': edges, 'svg': svg,
                      'nativeDiagram': native, 'renderChecks': checks, 'readingRows': reading_rows})
    from sysml_reader_custom import matrix_view
    views.extend(matrix_view(v) for v in list(views) if v['family'] == 'connections')
    from catalogue import canonicalize
    catalog = canonicalize(views)
    views = catalog['views']
    registry = json.loads((PACKAGE / 'sysml-view-map.json').read_text())
    routes = {concern: family for family in registry['families'] for concern in family['implemented']}
    for view in views:
        if view.get('standardView'):
            if view['family'] not in routes or routes[view['family']]['sysml']!=view['standardView']:
                raise ValueError('Semantic profile is absent from the view registry: '+view['family'])
            continue
        if view['family'] == 'exchanges':
            view['standardView'] = 'InterconnectionView'
        elif view['family'] in routes:
            view['standardView'] = routes[view['family']]['sysml']
        else:
            raise ValueError('No implemented standard view mapping: ' + view['family'])
    catalogue=json.loads((PACKAGE / 'mbse-view-profiles.json').read_text())
    groups={p['id']:p['group'] for p in catalogue['profiles']}
    aliases={'station-decomposition':'decomposition','station-structure':'connections','skid-detail':'connections',
             'motor-states':'state-transition','state-regions':'state-transition','capacity-requirement':'requirements',
             'capacity-verification':'verification','verification-coverage':'verification','exchange-summary':'exchanges',
             'trade-study':'analysis','interface-matrix':'connections'}
    for view in views:
        if view.get('svg'):
            from sysml_reader_binding import bind
            root=ET.fromstring(view['svg'])
            bind(root,view['nodes'],view['edges'],view_id=view['id'],revision=report['sourceSha256'])
            view['svg']=ET.tostring(root,encoding='unicode')
        profile=aliases.get(view['family'],aliases.get(view['id'],view['family']))
        view['group']=groups.get(profile,'Architecture')
    return {'schemaVersion': 1, 'role': 'semantic-model-reader', 'sourceSha256': report['sourceSha256'],
            'reportSha256': report['reportIntegrity']['reportSha256'],
            'sourceName': source_name, 'source': source, 'evidence': evidence, 'views': views,
            'viewAliases': catalog['aliases'], 'viewSummary': catalog['summary']}


def build(source: Path, report: Path, views: Path, output: Path, *, title='System model', replace=False, reader_config=None) -> dict:
    integrity, _, _ = specialist()
    source, report, views = source.resolve(), report.resolve(), views.resolve()
    output = output.absolute()
    inputs = (source, report, views) + ((Path(reader_config).resolve(),) if reader_config else ())
    if output.is_symlink() or any(p.is_relative_to(output.resolve()) for p in inputs):
        raise ValueError('Output may not alias or contain its inputs')
    marker = output / 'reader.json'
    if output.exists() and (not replace or not marker.is_file() or json.loads(marker.read_text()).get('role') != 'semantic-model-reader'):
        raise ValueError('Choose a new output directory or --replace an owned reader export')
    before = {p: p.read_bytes() for p in inputs}
    qualified = integrity.load_report(report, source=source)
    requests = json.loads(before[views])
    config = json.loads(before[inputs[-1]]) if reader_config else {}
    if not isinstance(config, dict):
        raise ValueError('Reader configuration must be an object')
    payload = project_views(qualified, requests, before[source].decode('utf-8'), source.name, labels=config.get('labels'))
    payload['title'] = title
    output.parent.mkdir(parents=True, exist_ok=True)
    lock = output.with_name(output.name + '.reader-lock')
    handle = lock.open('x')
    try:
        with tempfile.TemporaryDirectory(dir=output.parent, prefix='.model-reader-') as temp:
            stage = Path(temp) / 'export'
            stage.mkdir()
            (stage / 'reader.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
            (stage / 'model.sysml').write_bytes(before[source])
            (stage / 'views.json').write_bytes(before[views])
            if reader_config:
                (stage / 'reader-config.json').write_bytes(before[inputs[-1]])
            runtime = shutil.which('node')
            if not runtime:
                raise ValueError('Node.js 18 or newer is required')
            subprocess.run([runtime, str(PACKAGE / 'semantic-reader.mjs'), str(stage / 'reader.json'),
                            str(stage / 'index.html')], check=True, capture_output=True, text=True, timeout=120)
            # Recheck the complete managed receipt and all caller inputs before
            # publication. A concurrent model edit cannot produce mixed views.
            integrity.load_report(report, source=source)
            if any(p.read_bytes() != raw for p, raw in before.items()):
                raise ValueError('Model, report or view recipes changed during export')
            (stage / 'LICENSES.txt').write_text((PACKAGE / 'upstream/LICENSE').read_text() + '\n' +
                                               (PACKAGE / 'upstream/THIRD_PARTY_NOTICES.md').read_text())
            old = Path(temp) / 'previous'
            if output.exists():
                output.rename(old)
            try:
                stage.rename(output)
            except BaseException:
                if old.exists():
                    old.rename(output)
                raise
    finally:
        handle.close()
        lock.unlink(missing_ok=True)
    return {'ok': True, 'html': str(output / 'index.html'), 'views': len(payload['views']),
            'sourceSha256': payload['sourceSha256'], 'browserReview': 'pending'}
