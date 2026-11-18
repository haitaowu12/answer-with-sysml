#!/usr/bin/env python3
"""Publish one generated scenario as a laid-out SysON 2026.11 review project."""
import argparse
from collections import Counter
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from uuid import uuid4
from zipfile import ZipFile

VIEW = 'Action Flow View'


class SysON:
    def __init__(self, url):
        parts = urlsplit(url)
        if parts.scheme not in ('http', 'https') or not parts.netloc or parts.query or parts.fragment:
            raise ValueError('Provide the base URL of the receiving SysON instance')
        self.url = url.rstrip('/')

    def gql(self, query, variables, source=None):
        endpoint = '/api/graphql'
        operations = json.dumps({'query': query, 'variables': variables}).encode()
        headers = {'Content-Type': 'application/json'}
        body = operations
        if source is not None:
            endpoint += '/upload'
            boundary = uuid4().hex
            headers = {'Content-Type': 'multipart/form-data; boundary=' + boundary}
            fields = [
                ('operations', '', operations),
                ('map', '', b'{"0":"variables.file"}'),
                ('0', '; filename="model.sysml"\r\nContent-Type: text/plain', source),
            ]
            body = b''.join(
                f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"{extra}\r\n\r\n'.encode()
                + value + b'\r\n' for name, extra, value in fields
            ) + f'--{boundary}--\r\n'.encode()
        with urlopen(Request(self.url + endpoint, body, headers), timeout=120) as response:
            payload = response.read()
            try:
                result = json.loads(payload)
            except ValueError as error:
                raise ValueError(f'{endpoint} returned {response.status} without a JSON result '
                                 f'({response.headers.get("Content-Type", "no content type")})') from error
        if result.get('errors'):
            raise ValueError(str(result['errors']))
        return result['data']

    def mutate(self, name, input_type, fields, result_fragment='', source=None):
        error = '... on ErrorPayload { messages { body } }'
        result = self.gql(
            f'mutation($input:{input_type}!){{{name}(input:$input){{__typename {result_fragment} {error}}}}}',
            {'input': {'id': str(uuid4()), **fields}}, source,
        )[name]
        if result['__typename'] == 'ErrorPayload':
            raise ValueError(f'{name}: {result["messages"]}')
        return result

    def diagram(self, project_id, representation_id):
        with urlopen(f'{self.url}/api/projects/{project_id}', timeout=120) as response:
            data = response.read()
        with ZipFile(BytesIO(data)) as project:
            (path,) = [n for n in project.namelist()
                       if n.endswith(f'/representations/{representation_id}.json')]
            return json.loads(project.read(path))


def native_label(qualified_name):
    leaf = qualified_name.rsplit('::', 1)[-1]
    if "'" in qualified_name:
        # Match the final quoted SysML identifier, including escaped quotes.
        match = re.search(r"::'((?:\\.|[^'\\])*)'$", qualified_name)
        if match:
            return re.sub(r'\\(.)', r'\1', match[1])
    return leaf


def model_view(candidate, scenario_id, plan):
    source = (candidate / 'model.sysml').read_bytes()
    bindings = json.loads((candidate / 'bindings.json').read_text())
    recipe = json.loads((candidate / 'architecture.json').read_text())
    revision = hashlib.sha256(source).hexdigest()
    canonical = json.dumps(recipe, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    if revision != bindings['modelSha256'] or hashlib.sha256(canonical).hexdigest() != bindings['recipeSha256']:
        raise ValueError('Regenerate the model and bindings from the same architecture recipe')
    scenario = next((row for row in recipe['scenarios'] if row['id'] == scenario_id), None)
    if scenario is None:
        raise ValueError(f'Unknown scenario {scenario_id}')
    if scenario.get('parallelGroups'):
        raise ValueError('This SysON layout profile supports scenarios without explicit fork/join groups')
    elements = bindings['elements']
    names = {step['id']: native_label(elements[f'{scenario_id}/{step["id"]}']['qualifiedName'])
             for step in scenario['steps']}
    if len(set(names.values())) != len(names) or {'start', 'done'} & set(names):
        raise ValueError('Action display names must identify distinct nodes')
    if {'start', 'done'} & names.keys():
        raise ValueError('Step IDs start and done are reserved in the layout')
    names.update(start='start', done='done')
    transitions = scenario.get('transitions', [])
    exits = scenario.get('exitSteps', sorted(set(names) - {'start', 'done'} - {t['from'] for t in transitions}))
    edges = [(t['id'], t['from'], t['to'], native_label(elements[t['id']]['qualifiedName']), t.get('condition'))
             for t in transitions]
    edges += [('exit:' + end, end, 'done', None,
               scenario.get('exitGuards', {}).get(end)) for end in sorted(set(exits))]
    edges.append(('entry', 'start', scenario.get('entryStep', scenario['steps'][0]['id']), None, None))
    positions = plan['positions']
    if set(positions) != set(names):
        raise ValueError(f'Layout positions must match these IDs: {", ".join(names)}')
    offsets = plan.get('conditionOffsets', {})
    guarded_edges = {key for key, *_, guard in edges if guard}
    if offsets.keys() - guarded_edges:
        raise ValueError(f'Condition offsets must identify guarded edges: {", ".join(sorted(guarded_edges))}')
    for key, point in [*positions.items(), *offsets.items()]:
        if not isinstance(point, list) or len(point) != 2 or not all(
            isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) for n in point
        ):
            raise ValueError(f'Invalid layout position for {key}')
    return source, revision, native_label(elements[scenario_id]['qualifiedName']), scenario['label'], names, edges


def layout_diagram(diagram, names, edges, plan):
    scene_nodes = diagram['nodes']
    by_name = {node['targetObjectLabel']: node for node in scene_nodes}
    if set(by_name) != set(names.values()) or len(by_name) != len(scene_nodes):
        raise ValueError('SysON action topology differs from the selected source scenario')
    node_ids = {key: by_name[label]['id'] for key, label in names.items()}
    by_id = {node['id']: node for node in scene_nodes}
    nodes = []
    for key, (x, y) in plan['positions'].items():
        node = by_id[node_ids[key]]
        is_action = key not in ('start', 'done')
        # Default SysON action height is too short for wrapped usage/type names.
        width, height = (194, 102) if is_action else (node['defaultWidth'], node['defaultHeight'])
        nodes.append({
            'id': node['id'], 'position': {'x': x - width / 2, 'y': y - height / 2},
            'size': {'width': width, 'height': height},
            'resizedByUser': is_action, 'movedByUser': True, 'handleLayoutData': [],
            'minComputedSize': {'width': 0, 'height': 0},
        })

    def edge_key(edge):
        return (edge['sourceId'], edge['targetId'],
                edge['centerLabel']['text'] if edge.get('centerLabel') else '')

    edge_keys = Counter(edge_key(edge) for edge in diagram['edges'])
    expected = Counter()
    labels = []
    for key, start, end, name, guard in edges:
        candidates = [e for e in diagram['edges']
                      if e['sourceId'] == node_ids[start] and e['targetId'] == node_ids[end]
                      and (name is None or e['targetObjectLabel'] == name)]
        guard_text = ' '.join(guard.replace('\x00', '').split()) if guard else ''
        matches = [e for e in candidates if edge_key(e)[2] == (f'[{guard_text}]' if guard else '')
                   or edge_key(e)[2] == f'[{guard_text} ({key})]'
                   or (key.startswith('exit:') and
                       edge_key(e)[2] == f'[{guard_text} (completion {start})]')]
        if len(matches) != 1:
            raise ValueError(f'SysON did not preserve the expected branch {start} → {end}: {guard or "unguarded"}')
        match = matches[0]
        expected[edge_key(match)] += 1
        if key in plan.get('conditionOffsets', {}):
            x, y = plan['conditionOffsets'][key]
            labels.append({
                'id': match['centerLabel']['id'], 'position': {'x': x, 'y': y},
                'size': {'width': 0, 'height': 0}, 'resizedByUser': False, 'movedByUser': True,
            })
    if edge_keys != expected:
        raise ValueError('SysON contains connections outside the selected scenario')
    return dict(nodeLayoutData=nodes, edgeLayoutData=[], labelLayoutData=labels, autoLayoutState='ACTIVATE')


def publish(client, candidate, scenario, layout, project_name):
    plan = json.loads(layout.read_text())
    source, revision, action, label, names, edges = model_view(candidate, scenario, plan)
    title = plan.get('name') or f'{label} ({scenario})'

    project = client.mutate('createProject', 'CreateProjectInput',
                            dict(name=project_name, templateId='blank-project', libraryIds=[]),
                            '... on CreateProjectSuccessPayload { project { id } }')['project']['id']
    print(f'Created review project {client.url}/projects/{project}/edit', flush=True)
    query = 'query($p:ID!){viewer{project(projectId:$p){currentEditingContext{id}}}}'
    context = client.gql(query, {'p': project})['viewer']['project']['currentEditingContext']['id']
    imported = client.mutate('uploadDocument', 'UploadDocumentInput',
                             dict(editingContextId=context, readOnly=False, file=None),
                             '... on UploadDocumentSuccessPayload { report }', source=source)
    search = '''query($c:ID!,$text:String!){
      viewer{editingContext(editingContextId:$c){search(query:{text:$text,matchCase:true,
      matchWholeWord:true,useRegularExpression:false,searchInAttributes:false,searchInLibraries:false}){
      ... on SearchSuccessPayload{result{matches{id label kind}}}}}}}'''
    found = client.gql(search, {'c': context, 'text': action})
    (scope,) = [obj['id'] for obj in found['viewer']['editingContext']['search']['result']['matches']
                if obj['label'] == action and obj['kind'].endswith('entity=ActionUsage')]
    descriptions = '''query($c:ID!,$scope:ID!){viewer{editingContext(editingContextId:$c){
      representationDescriptions(objectId:$scope){edges{node{id label}}}}}}'''
    choices = client.gql(descriptions, {'c': context, 'scope': scope})
    (description,) = [edge['node']['id'] for edge in choices['viewer']['editingContext']
                      ['representationDescriptions']['edges'] if edge['node']['label'] == VIEW]
    representation = client.mutate(
        'createRepresentation', 'CreateRepresentationInput',
        dict(editingContextId=context, objectId=scope, representationDescriptionId=description,
             representationName=title),
        '... on CreateRepresentationSuccessPayload { representation { id label } }',
    )['representation']['id']
    palette = '''query($c:ID!,$r:ID!){viewer{editingContext(editingContextId:$c){
      representation(representationId:$r){description{... on DiagramDescription{
      palette(diagramElementIds:[$r]){paletteEntries{... on ToolSection{label tools{id label}}}}}}}}}}'''
    sections = client.gql(palette, {'c': context, 'r': representation})['viewer']['editingContext'][
        'representation']['description']['palette']['paletteEntries']
    (tool,) = [t['id'] for section in sections if section.get('label') == 'Related Elements'
               for t in section['tools'] if t['label'] == 'Add existing elements']
    client.mutate('invokeSingleClickOnDiagramElementTool', 'InvokeSingleClickOnDiagramElementToolInput',
                  dict(editingContextId=context, representationId=representation,
                       diagramElementIds=[representation], variables=[], startingPositionX=0,
                       startingPositionY=0, toolId=tool))
    snapshot = client.diagram(project, representation)
    diagram = snapshot['representation']
    geometry = layout_diagram(diagram, names, edges, plan)
    client.mutate('layoutDiagram', 'LayoutDiagramInput',
                  dict(editingContextId=context, representationId=representation,
                       cause='layout', diagramLayoutData=geometry))
    saved = client.diagram(project, representation)
    saved_layout = saved['representation']['layoutData']
    if saved['label'] != title or any(
        saved_layout[group].get(item['id'], {}).get('position') != item['position']
        for group in ('nodeLayoutData', 'labelLayoutData') for item in geometry[group]
    ):
        raise ValueError('SysON did not persist the named diagram and generated positions')
    return dict(name=title, url=f'{client.url}/projects/{project}/edit/{representation}',
                modelSha256=revision, scenario=scenario, actions=len(names) - 2,
                connections=len(edges), conditions=sum(bool(edge[-1]) for edge in edges),
                importReport=imported['report'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--scenario', required=True)
    parser.add_argument('--layout', type=Path, required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--project-name', required=True)
    args = parser.parse_args()
    result = publish(SysON(args.url), args.candidate, args.scenario, args.layout, args.project_name)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (KeyError, OSError, ValueError) as error:
        raise SystemExit(f'SysON review generation failed: {error}')
