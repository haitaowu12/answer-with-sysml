"""One canonical presentation for each exact global semantic inventory page.

Model and requirement catalogues are evidence indexes. Repeating an index under
another navigation scope does not make another architecture view. This module
compares source-bound semantic payloads, not titles or overlapping element IDs.
It never merges scoped architecture views or interprets SysML text.
"""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path


GLOBAL_INVENTORIES = frozenset({'model-catalogue', 'requirement-catalogue'})
# These fields describe navigation or derived artwork. Every other field,
# including unfamiliar future semantic fields, participates in comparison.
NAVIGATION_FIELDS = frozenset({
    'id', 'label', 'title', 'group', 'scope', 'readerScope',
    'svg', 'notation', 'nativeDiagram', 'renderChecks',
})
PROJECTION_SCOPE_FIELDS = frozenset({'id', 'scopeElementId'})


def semantic_signature(view):
    """Return a signature only for a complete, revision-bound global inventory.

The two reserved catalogue families are global in the existing reader format.
A scoped catalogue must declare catalogueScope='local'; it is never collapsed.
Other view families always remain distinct, even when they share elements.
    """
    if view.get('family') not in GLOBAL_INVENTORIES or view.get('catalogueScope', 'global') != 'global':
        return None
    revision = view.get('sourceSha256')
    if (not isinstance(view.get('question'), str) or not view['question'].strip()
            or not isinstance(revision, str) or len(revision) != 64
            or any(c not in '0123456789abcdef' for c in revision.lower())
            or not isinstance(view.get('nodes'), list) or not isinstance(view.get('edges'), list)
            or not isinstance(view.get('catalogueRows'), list)):
        # A manifest or element selection alone cannot establish equivalence.
        return None
    semantics = {k: v for k, v in view.items() if k not in NAVIGATION_FIELDS}
    if isinstance(semantics.get('projection'), dict):
        semantics['projection'] = {k: v for k, v in semantics['projection'].items()
                                   if k not in PROJECTION_SCOPE_FIELDS}
    raw = json.dumps(semantics, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def canonicalize(views):
    """Keep first appearances and retain navigation aliases for exact duplicates.

Inputs are unmodified. Ordering within semantic arrays is intentional: changing
row or relation order is not silently treated as an identical presentation.
Aliases preserve access from every original scope and can redirect old view IDs.
    """
    if not isinstance(views, list) or any(not isinstance(v, dict) for v in views):
        raise ValueError('Views must be an array of semantic presentation objects')
    identifiers = [v.get('id') for v in views]
    if any(not isinstance(v, str) or not v for v in identifiers) or len(set(identifiers)) != len(identifiers):
        raise ValueError('View IDs must be nonempty and unique before canonicalization')
    canonical, aliases, seen = [], [], {}
    for view in views:
        signature = semantic_signature(view)
        if signature is not None and signature in seen:
            aliases.append(dict(id=view['id'], canonicalId=seen[signature],
                                label=view.get('label', view.get('title', view['id'])),
                                scope=view.get('scope'), readerScope=view.get('readerScope'),
                                reason='Exact global inventory duplicate', semanticSha256=signature))
        else:
            canonical.append(deepcopy(view))
            if signature is not None:
                seen[signature] = view['id']
    return dict(views=canonical, aliases=aliases,
                summary=dict(inputViews=len(views), canonicalViews=len(canonical), duplicateViews=len(aliases)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--views', required=True, type=Path, help='JSON array of full semantic view payloads')
    parser.add_argument('--output', required=True, type=Path, help='New JSON file with canonical views and aliases')
    args = parser.parse_args()
    result = canonicalize(json.loads(args.views.read_text()))
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
