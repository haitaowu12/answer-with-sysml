#!/usr/bin/env python3
"""Render explorable diagrams with the bundled Archify engine and explicit outputs.

Uses native input/artifact checks. Browser inspection belongs to the in-app browser;
this adapter never launches a browser, installs dependencies or checks for updates.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'resources/tools/archify'
ENGINE = PACKAGE / 'upstream'
CLI = ENGINE / 'bin/archify.mjs'
SYSML = ROOT / '.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/scripts/sysml.py'
EXAMPLES = {
    'architecture': 'web-app.architecture.json',
    'workflow': 'agent-tool-call.workflow.json',
    'sequence': 'cache-miss-request.sequence.json',
    'dataflow': 'product-analytics.dataflow.json',
    'lifecycle': 'deployment-release.lifecycle.json',
    'erd': 'orders.erd.json',
    'class': 'payments.class.json',
    'tree': 'payment-platform.tree.json',
    'timeline': 'payment-incident.timeline.json',
    'waterfall': 'checkout-request.waterfall.json',
}


class EngineError(ValueError):
    def __init__(self, receipt: dict):
        self.receipt = receipt
        super().__init__(receipt.get('error', 'Archify checks failed'))


def read_spec(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(spec, dict) or spec.get('diagram_type') not in EXAMPLES:
        raise ValueError('Input must name one of the ten supported diagram_type values')
    if not isinstance(spec.get('meta'), dict):
        raise ValueError('Input must contain a meta object')
    return spec


def run_engine(args: list[str], cwd: Path, *, structured: bool = True):
    node = shutil.which('node')
    if not node:
        raise ValueError('Node.js 18 or newer is required; no dependency installation is needed')
    result = subprocess.run(
        [node, str(CLI), *args], cwd=cwd,
        env={**os.environ, 'ARCHIFY_UPDATE_CHECK_DISABLED': '1'},
        capture_output=True, text=True, timeout=120,
    )
    if not structured:
        if result.returncode:
            raise ValueError(result.stderr.strip() or result.stdout.strip())
        return result.stdout
    try:
        receipt = json.loads(result.stdout)
    except ValueError as error:
        raise EngineError({'ok': False, 'error': 'Engine returned no complete JSON receipt: '
                           + result.stderr[:1200],
                           'recoveryRequired': args[0] in ('deliver', 'compare')}) from error
    if result.returncode or receipt.get('ok') is False:
        raise EngineError(receipt)
    return receipt


def write_json(path: Path, value: dict) -> None:
    """Replace a single owned sidecar without exposing a partial JSON document."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix='.diagram-', delete=False) as handle:
        temporary = Path(handle.name)
        try:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def html_path(path: Path) -> Path:
    path = path.absolute()
    if path.suffix.lower() != '.html':
        raise ValueError('Output must be an explicit .html file')
    # The native engine also checks physical aliases. Reject named symlink
    # outputs here before the adapter writes any editable-source sidecar.
    if path.is_symlink():
        raise ValueError('Output may not be a symbolic link')
    return path


def needs_native_recovery(value) -> bool:
    # These native diagnostics retain ownership or an unfinished transaction.
    # Restoring our snapshot here could erase its journal or another claimant's
    # bytes. Preserve them for explicit native recovery; never remove its locks.
    ownership_codes = {
        'delivery/lock-stale', 'delivery/lock-invalid', 'delivery/lock-release',
        'delivery/ownership-lost', 'delivery/concurrent-attempt',
        'delivery/legacy-pending', 'delivery/provenance-locked',
    }
    if isinstance(value, dict):
        code = str(value.get('code', '')).lower()
        if value.get('recoveryRequired') is True or 'recovery' in code or code in ownership_codes:
            return True
        return any(needs_native_recovery(item) for item in value.values())
    if isinstance(value, list):
        return any(needs_native_recovery(item) for item in value)
    return False


@contextmanager
def output_attempt(paths: list[Path], *, replace: bool):
    """Rollback our named artifacts on ordinary failure, including native sidecars.

    Native delivery owns its crash journal and atomic HTML publication. This
    context adds rollback for the adapter's source/review files; it is not a
    multi-file crash transaction or coordination with unrelated native writers.
    """
    paths[0].parent.mkdir(parents=True, exist_ok=True)
    lock = paths[0].with_suffix('.adapter-lock')
    handle = lock.open('x')
    try:
        snapshots = {}
        for path in paths:
            if path.is_symlink() or (path.exists() and not path.is_file()):
                raise ValueError('Output sidecar is not a regular file: ' + str(path))
            if path.exists() and not replace:
                raise ValueError('Output exists; use --replace for an intentional revision: ' + str(path))
            snapshots[path] = (path.read_bytes(), path.stat().st_mode) if path.exists() else None
        try:
            yield
        except BaseException as error:
            if isinstance(error, (KeyboardInterrupt, subprocess.TimeoutExpired)):
                raise
            if isinstance(error, EngineError) and needs_native_recovery(error.receipt):
                # A native rollback/ownership failure may retain the only
                # recoverable bytes. Preserve that evidence for its recovery path.
                raise
            for path, previous in snapshots.items():
                if previous is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(previous[0])
                    path.chmod(previous[1])
            raise
    finally:
        handle.close()
        lock.unlink(missing_ok=True)


def repository_args(repo: Path | None) -> list[str]:
    return ['--repo-root', str(repo.resolve())] if repo else []


def render(source: Path, output: Path, *, repo: Path | None = None,
           quality: str | None = None, replace: bool = False,
           model_evidence: dict | None = None) -> dict:
    spec = read_spec(source)
    output = html_path(output)
    editable = output.with_suffix('.source.json')
    delivery = output.with_suffix('.delivery.json')
    pending = output.with_suffix('.delivery-pending.json')
    review = output.with_suffix('.review.json')
    model = output.with_suffix('.model.json')
    if source.resolve() in {p.resolve() for p in (output, delivery, pending, review, model)}:
        raise ValueError('Input may not alias the HTML or a verification sidecar')
    profile = quality or spec['meta'].get('quality_profile', 'showcase')
    if profile not in ('standard', 'showcase'):
        raise ValueError('Quality must be standard or showcase')
    # Normalize transport metadata only. Never alter nodes, edges, conditions,
    # source ranges or user-selected presentation to satisfy a layout check.
    spec['meta']['output'] = output.name
    spec['meta']['quality_profile'] = profile
    paths = [output, editable, delivery, review, pending]
    if model_evidence is not None:
        paths.append(model)
    elif model.exists():
        raise ValueError('Model-derived output must be revised through sysml-hierarchy')
    with output_attempt(paths, replace=replace):
        write_json(editable, spec)
        delivered = run_engine(['deliver', spec['diagram_type'], str(editable), str(output),
                                '--quality', profile, *repository_args(repo), '--json'], output.parent)
        checked = run_engine(['check', str(output), '--require-provenance', '--json'], output.parent)
        if model_evidence is not None:
            write_json(model, model_evidence)
        result = {
            'schemaVersion': 1, 'ok': True, 'command': 'render',
            'engine': json.loads((PACKAGE / 'SOURCE.json').read_text(encoding='utf-8')),
            'html': str(output), 'source': str(editable),
            'delivery': delivered, 'artifactCheck': checked,
            'browserReview': {'status': 'pending', 'method': 'Codex in-app browser',
                              'boundary': 'No browser or perceptual check was executed by this command.'},
        }
        write_json(review, result)
    return {'ok': True, 'html': str(output), 'source': str(editable), 'review': str(review),
            'automatedChecks': 'passed', 'browserReview': 'pending'}


def hierarchy_spec(projection: dict) -> dict:
    """Project ownership only; never turn transitions or flows into containment."""
    if projection.get('profile') != 'declared-behavior-v1':
        raise ValueError('Unsupported SysML projection profile')
    nodes = projection.get('nodes', [])
    if not nodes or len({n['id'] for n in nodes}) != len(nodes):
        raise ValueError('Missing or duplicate model identities')
    identities = {n['id']: 'm' + hashlib.sha256(n['id'].encode()).hexdigest() for n in nodes}
    by_id = {n['id']: n for n in nodes}
    root = by_id.get(projection.get('rootId'))
    if root is None:
        raise ValueError('Model root is absent')
    labels = {'StateDefinition': 'State definition', 'StateUsage': 'State',
              'ExhibitStateUsage': 'Exhibited state', 'ActionDefinition': 'Action definition',
              'ActionUsage': 'Action', 'PerformActionUsage': 'Performed action',
              'EntryAction': 'Entry action',
              'ActionBoundary': 'Action boundary', 'EntryDeclaration': 'Entry declaration'}
    rendered = []
    for node in nodes:
        if node['kind'] not in labels:
            raise ValueError('Unsupported model kind: ' + node['kind'])
        sublabel = labels[node['kind']]
        if node['kind'] in ('StateDefinition', 'StateUsage', 'ExhibitStateUsage'):
            sublabel += (' · concurrent regions' if node.get('parallel') is True else
                         ' · parallelism unknown' if node.get('parallel') is None else '')
        item = {'id': identities[node['id']], 'label': node['name'], 'sublabel': sublabel}
        if node.get('parent') is not None:
            if node['parent'] not in identities:
                raise ValueError('Model parent is outside the selected scope')
            item['parent'] = identities[node['parent']]
        rendered.append(item)
    partial = projection.get('coverage') == 'partial'
    return {'schema_version': 1, 'diagram_type': 'tree',
            'meta': {'title': root['name'] + ' — behavior hierarchy',
                     'subtitle': 'Connectors show ownership. Transitions, conditions and timing are outside this view.',
                     'animation': 'none'},
            'layout': {'direction': 'right'}, 'nodes': rendered,
            'cards': [{'dot': 'orange' if partial else 'emerald', 'title': 'Model scope',
                       'items': [('Partial coverage of the selected local declarations.' if partial else
                                  'Selected local state and action declarations.') +
                                 ' Inherited behavior is not expanded. This is a model view, not an execution result.']}]}


def sysml_hierarchy(source: Path, report: Path, target: str, output: Path, *,
                    replace: bool = False) -> dict:
    """Use the specialist's managed-report boundary, without parsing SysML text."""
    output = html_path(output)
    reserved = [output, *(output.with_suffix(suffix) for suffix in
                          ('.source.json', '.delivery.json', '.delivery-pending.json', '.review.json', '.model.json'))]
    if any(p.resolve() in {q.resolve() for q in reserved} for p in (source, report)):
        raise ValueError('Output may not alias a model input')
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (source, report)}
    with tempfile.TemporaryDirectory(prefix='model-hierarchy-') as temp:
        projection_path = Path(temp) / 'projection.json'
        result = subprocess.run([sys.executable, '-B', str(SYSML), 'explain', '--source', str(source.resolve()),
                                 '--report', str(report.resolve()), '--target', target,
                                 '--output', str(projection_path)], capture_output=True, text=True, timeout=90)
        if result.returncode:
            raise ValueError('SysML projection refused: ' + (result.stderr or result.stdout)[-1800:])
        projection = json.loads(projection_path.read_text())
        if any(hashlib.sha256(p.read_bytes()).hexdigest() != digest for p, digest in before.items()):
            raise ValueError('Model inputs changed during projection')
        if (projection.get('sourceSha256') != before[source] or projection.get('reportSha256') != before[report]
                or projection.get('target') != target):
            raise ValueError('SysML projection revision or target mismatch')
        spec = hierarchy_spec(projection)
        candidate = Path(temp) / 'hierarchy.json'
        write_json(candidate, spec)
        evidence = {'projection': projection, 'sourceFile': str(source.resolve()),
                    'reportFile': str(report.resolve()),
                    'nodeIds': {n['id']: 'm' + hashlib.sha256(n['id'].encode()).hexdigest()
                                for n in projection['nodes']},
                    'view': 'Ownership hierarchy only; relations and conditions retained here, not drawn as tree edges.'}
        return render(candidate, output, replace=replace, model_evidence=evidence)


def compare(base: Path, head: Path, output: Path, *, repo: Path | None = None,
            quality: str = 'showcase', replace: bool = False) -> dict:
    for source in (base, head):
        if read_spec(source)['diagram_type'] != 'architecture':
            raise ValueError('Architecture comparison requires two architecture inputs')
    output = html_path(output)
    if output.with_suffix('.model.json').exists():
        raise ValueError('Model-derived output must be revised through sysml-hierarchy')
    receipt = output.with_suffix('.delta.json')
    if any(p.resolve() in (output.resolve(), receipt.resolve()) for p in (base, head)):
        raise ValueError('Comparison output may not alias its inputs')
    with output_attempt([output, receipt], replace=replace):
        result = run_engine(['compare', 'architecture', str(base.resolve()), str(head.resolve()),
                             str(output), '--receipt', str(receipt), '--quality', quality,
                             *repository_args(repo), '--json'], output.parent)
    return {'ok': True, 'html': str(output), 'receipt': str(receipt),
            'comparison': result, 'browserReview': 'pending'}


def preview(source: Path, output: Path, *, repo: Path | None = None,
            quality: str | None = None, replace: bool = False) -> int:
    result = render(source, output, repo=repo, quality=quality, replace=replace)
    editable = Path(result['source'])
    spec = read_spec(editable)
    print(json.dumps({**result, 'editToRefresh': str(editable),
                      'note': 'Native loopback preview follows; open its printed URL in iab. '
                              'The initial review receipt is not refreshed by live updates.'}), flush=True)
    node = shutil.which('node')
    return subprocess.run(
        [node, str(CLI), 'preview', spec['diagram_type'], str(editable), str(output.absolute()),
         '--no-open', '--quality', spec['meta']['quality_profile'], *repository_args(repo)],
        cwd=output.absolute().parent,
        env={**os.environ, 'ARCHIFY_UPDATE_CHECK_DISABLED': '1'},
    ).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('types', help='Show supported types and exact reference paths')
    sub.add_parser('doctor', help='Check the installed production runtime without a browser')
    guide = sub.add_parser('guide', help='Select a diagram type from a scenario')
    guide.add_argument('scenario')
    for command in ('schema', 'example'):
        p = sub.add_parser(command)
        p.add_argument('type', choices=EXAMPLES)
    for command in ('render', 'validate', 'preview'):
        p = sub.add_parser(command)
        p.add_argument('input', type=Path)
        p.add_argument('--repo-root', type=Path)
        p.add_argument('--quality', choices=('standard', 'showcase'))
        if command in ('render', 'preview'):
            p.add_argument('--output', type=Path, required=True)
            p.add_argument('--replace', action='store_true')
    p = sub.add_parser('check', help='Strict native artifact/provenance check; no browser')
    p.add_argument('html', type=Path)
    p = sub.add_parser('compare', help='Exact-ID Architecture Before / Delta / After')
    p.add_argument('base', type=Path)
    p.add_argument('head', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--repo-root', type=Path)
    p.add_argument('--quality', choices=('standard', 'showcase'), default='showcase')
    p.add_argument('--replace', action='store_true')
    p = sub.add_parser('gsn-reader', help='GSN v3 core argument in the shared interactive reader')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--title', default='Assurance argument')
    p.add_argument('--replace', action='store_true')
    p = sub.add_parser('sysml-reader', help='One clean reader over qualified semantic views')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--views', type=Path, required=True)
    p.add_argument('--reader-config', type=Path, help='Optional reader configuration containing qualified-name labels')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--title', default='System model')
    p.add_argument('--replace', action='store_true')
    p = sub.add_parser('sysml-hierarchy', help='Ownership view from a managed SysML state/action report')
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--target', required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'types':
            result = {kind: {'schema': str(ENGINE / f'schemas/{kind}.schema.json'),
                             'commonSchema': str(ENGINE / 'schemas/common.schema.json'),
                             'example': str(ENGINE / 'examples' / example),
                             'reference': str(ENGINE / ('references/authoring-contract.md'
                                                       if kind == 'architecture' else f'renderers/{kind}/README.md'))}
                      for kind, example in EXAMPLES.items()}
        elif args.command in ('schema', 'example'):
            path = ENGINE / (f'schemas/{args.type}.schema.json' if args.command == 'schema'
                             else 'examples/' + EXAMPLES[args.type])
            result = json.loads(path.read_text(encoding='utf-8'))
        elif args.command == 'doctor':
            print(run_engine(['doctor'], ROOT, structured=False), end='')
            return 0
        elif args.command == 'guide':
            result = run_engine(['guide', args.scenario, '--json'], ROOT)
        elif args.command == 'render':
            result = render(args.input, args.output, repo=args.repo_root,
                            quality=args.quality, replace=args.replace)
        elif args.command == 'preview':
            return preview(args.input, args.output, repo=args.repo_root,
                           quality=args.quality, replace=args.replace)
        elif args.command == 'validate':
            spec = read_spec(args.input)
            result = run_engine(['validate', spec['diagram_type'], str(args.input.resolve()),
                                 *(['--quality', args.quality] if args.quality else []),
                                 *repository_args(args.repo_root), '--json'], args.input.resolve().parent)
        elif args.command == 'check':
            result = run_engine(['check', str(args.html.resolve()), '--require-provenance', '--json'],
                                args.html.resolve().parent)
        elif args.command == 'sysml-hierarchy':
            result = sysml_hierarchy(args.source, args.report, args.target, args.output, replace=args.replace)
        elif args.command == 'gsn-reader':
            from gsn_reader import build
            result = build(args.source, args.output, title=args.title, replace=args.replace)
        elif args.command == 'sysml-reader':
            from sysml_reader import build
            result = build(args.source, args.report, args.views, args.output, title=args.title, replace=args.replace,
                           reader_config=args.reader_config)
        else:
            result = compare(args.base, args.head, args.output, repo=args.repo_root,
                             quality=args.quality, replace=args.replace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except EngineError as error:
        print(json.dumps(error.receipt, ensure_ascii=False, indent=2))
        return 1
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False))
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == '__main__':
    sys.exit(main())
