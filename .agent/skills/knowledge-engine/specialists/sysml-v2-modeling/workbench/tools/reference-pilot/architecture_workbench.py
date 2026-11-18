#!/usr/bin/env python3
"""Build one reviewable architecture candidate, retaining separate evidence stages.

Input is an authored engineering recipe, not raw prose. A successful run creates
a candidate for engineering review; it never executes a verification case or
accepts a design. Existing output is refused and failed stages are retained.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from architecture_check import check_architecture, main as check_main
from architecture_model import build as build_model


TOOLS = Path(__file__).resolve().parent


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(architecture, output, package='ConOpsArchitecture', qualify=False,
        jar=None, library=None, evidence=None, reader=True):
    architecture, output = Path(architecture), Path(output)
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Use a new output directory; prior candidates and evidence are preserved')
    if qualify and (not jar or not library):
        raise ValueError('Native qualification requires the locked --jar and --library')
    raw = architecture.read_bytes()
    packet = json.loads(raw)
    authored = check_architecture(packet)
    result = {'schemaVersion': 1, 'status': 'building', 'stages': {},
              'inputSha256': hashlib.sha256(raw).hexdigest(),
              'engineeringAcceptance': 'not-assessed',
              'verificationExecution': 'not-run',
              'boundary': 'A candidate architecture and its translation checks; no source-meaning, design approval or executed service-performance claim.'}
    output.mkdir(parents=True, exist_ok=True)

    def finish(status, code):
        result['status'] = status
        if 'model' in result:
            result['model']['languageValidation'] = result['stages'].get('nativeLanguage', 'not-run')
        write_json(output / 'build-result.json', result)
        return result, code

    def failed(stage, error):
        result['stages'][stage] = 'failed'
        result['error'] = str(error)
        if not (output / 'input.snapshot.json').exists():
            (output / 'input.snapshot.json').write_bytes(raw)
        return finish('blocked-' + stage, 2)

    result['stages']['authoredConsistency'] = 'passed' if authored['structuralConsistencyPassed'] else 'failed'
    result['reviewReadiness'] = authored['reviewReadiness']
    if not authored['structuralConsistencyPassed']:
        (output / 'architecture.json').write_bytes(raw)
        authored['architectureSha256'] = hashlib.sha256(raw).hexdigest()
        write_json(output / 'architecture-checks.json', authored)
        return finish('blocked-invalid-architecture', 2)

    print('Authoring editable model and identity bindings', flush=True)
    try:
        result['model'] = build_model(packet, output, package)
        result['stages']['nativeAuthoring'] = 'passed'
        (output / 'input.snapshot.json').write_bytes(raw)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return failed('nativeAuthoring', error)
    check_args = ['--architecture', str(output / 'architecture.json'), '--output', str(output / 'architecture-checks.json')]
    if qualify:
        print('Qualifying candidate with the locked language runtime', flush=True)
        command = [sys.executable, '-B', str(TOOLS / 'qualify.py'),
                   '--source', str(output / 'model.sysml'), '--output', str(output / 'qualification'),
                   '--jar', str(jar), '--library', str(library)]
        try:
            with (output / 'qualification.log').open('w', encoding='utf-8') as log:
                completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        except (OSError, subprocess.SubprocessError) as error:
            return failed('nativeLanguage', error)
        result['stages']['nativeLanguage'] = 'passed' if completed.returncode == 0 else 'failed'
        if completed.returncode:
            check_main(check_args)
            return finish('blocked-native-language', 2)
        check_args += ['--model', str(output / 'model.sysml'),
                       '--native-report', str(output / 'qualification/report.json'),
                       '--bindings', str(output / 'bindings.json')]
    else:
        result['stages']['nativeLanguage'] = 'not-run'
    print('Reconciling authored relationships and native facts', flush=True)
    try:
        checked = check_main(check_args)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return failed('nativeReconciliation', error)
    result['stages']['nativeReconciliation'] = ('passed' if not checked else 'failed') if qualify else 'not-run'
    if checked:
        return finish('blocked-relationship-reconciliation', 2)
    if reader:
        from architecture_review import build as build_review
        print('Building question-led architecture reader', flush=True)
        try:
            result['reader'] = build_review(architecture=output / 'architecture.json',
                model=output / 'model.sysml', bindings=output / 'bindings.json', output=output,
                checks=output / 'architecture-checks.json', evidence=Path(evidence) if evidence else None)
        except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
            return failed('readerGeneration', error)
        result['stages']['readerGeneration'] = 'passed'
        result['stages']['readerInteraction'] = 'not-run'
    else:
        result['stages']['readerGeneration'] = 'not-run'
    result['model']['languageValidation'] = result['stages']['nativeLanguage']
    return finish('candidate-for-engineering-review', 0)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--architecture', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--package', default='ConOpsArchitecture')
    p.add_argument('--qualify', action='store_true')
    p.add_argument('--jar', type=Path)
    p.add_argument('--library', type=Path)
    p.add_argument('--evidence', type=Path, help='Optional retained source inventory for the evidence tab')
    p.add_argument('--no-reader', action='store_true', help='Build and check the native candidate without HTML')
    a = p.parse_args(argv)
    result, code = run(a.architecture, a.output, a.package, a.qualify, a.jar, a.library, a.evidence, not a.no_reader)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
