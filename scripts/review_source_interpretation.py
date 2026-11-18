#!/usr/bin/env python3
"""Check a source-first review receipt against its exact source and recipe.

Checks recorded expectations, not natural-language entailment or design approval.
"""
import argparse
import hashlib
import json
from pathlib import Path

FOCI = ('concurrency-outcomes', 'message-phases', 'boundary-exchanges', 'revision-identity')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pointer(document, path):
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('assertion path must be a JSON pointer')
    value = document
    for token in path[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not token.isdecimal():
                raise ValueError('array pointer requires a nonnegative index')
            value = value[int(token)]
        elif isinstance(value, dict):
            value = value[token]
        else:
            raise ValueError('pointer traverses a scalar')
    return value


def review(source_bytes, recipe_bytes, receipt):
    errors = []
    source = source_bytes.decode('utf-8')
    recipe = json.loads(recipe_bytes)
    if not isinstance(receipt, dict):
        return {'passed': False, 'errors': ['review must be an object']}
    if type(receipt.get('schemaVersion')) is not int or receipt['schemaVersion'] != 1:
        errors.append('schemaVersion must be 1')
    for name, data in [('source', source_bytes), ('recipe', recipe_bytes)]:
        if receipt.get(name+'Sha256') != digest(data):
            errors.append(name+' revision differs from reviewed bytes')
    if receipt.get('basis') != 'source-first-independent-review':
        errors.append('a source-first independent interpretation review is required')
    rows = receipt.get('checks')
    if not isinstance(rows, list):
        return {'passed': False, 'errors': errors+['checks must be a list']}
    seen, covered = set(), set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append('check must be an object'); continue
        key = row.get('id')
        if not isinstance(key, str) or not key.strip() or key in seen:
            errors.append('check IDs must be nonempty and unique')
        else:
            seen.add(key)
        focus = row.get('focus')
        if focus not in FOCI:
            errors.append(str(key)+': unknown review focus')
        else:
            covered.add(focus)
        if not isinstance(row.get('rationale'), str) or not row['rationale'].strip():
            errors.append(str(key)+': reviewer rationale is required')
        refs = row.get('sourceRefs')
        if not isinstance(refs, list) or not refs or any(not isinstance(r, str) or not r.strip() or r not in source for r in refs):
            errors.append(str(key)+': source locators must occur in the reviewed source')
        status = row.get('status')
        if status not in ('supported', 'not-applicable'):
            errors.append(str(key)+': interpretation remains unresolved')
            continue
        assertions = row.get('assertions')
        if status == 'not-applicable':
            if assertions:
                errors.append(str(key)+': not-applicable must not conceal assertions')
            continue
        if not isinstance(assertions, list) or not assertions:
            errors.append(str(key)+': supported review requires recipe assertions'); continue
        for assertion in assertions:
            try:
                if not isinstance(assertion, dict):
                    raise ValueError('assertion must be an object')
                actual = pointer(recipe, assertion.get('path'))
                kinds = [k for k in ('equals', 'containsIds') if k in assertion]
                if len(kinds) != 1:
                    raise ValueError('use exactly one assertion operator')
                if kinds[0] == 'equals':
                    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(assertion['equals'], sort_keys=True, allow_nan=False):
                        raise ValueError('value does not match source-review expectation')
                else:
                    ids = assertion['containsIds']
                    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or not i for i in ids):
                        raise ValueError('containsIds requires nonempty IDs')
                    if not isinstance(actual, list) or any(not isinstance(item, dict) for item in actual):
                        raise ValueError('containsIds target must be a list of records')
                    actual_ids = [item.get('id') for item in actual]
                    if any(actual_ids.count(i) != 1 for i in ids):
                        raise ValueError('required source interaction is missing or duplicated')
            except (ValueError, KeyError, IndexError, TypeError) as error:
                errors.append(str(key)+': '+str(error))
    for focus in FOCI:
        if focus not in covered:
            errors.append('unreviewed focus: '+focus)
    return {'passed': not errors, 'errors': errors,
            'scope': 'Review-receipt consistency only; source interpretation still requires independent judgment.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--recipe', type=Path, required=True)
    p.add_argument('--review', type=Path, required=True)
    args = p.parse_args()
    try:
        result = review(args.source.read_bytes(), args.recipe.read_bytes(), json.loads(args.review.read_text()))
    except (OSError, ValueError, UnicodeError) as error:
        result = {'passed': False, 'errors': [str(error)]}
    print(json.dumps(result, indent=2))
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
