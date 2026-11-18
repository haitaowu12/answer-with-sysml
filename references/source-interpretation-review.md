# Source interpretation review

Do this before delivery, independently of the authoring pass. A valid model can
still misrepresent its source. Freeze the source-derived questions and expected
answers before checking the proposed recipe; do not rewrite expectations merely
to make the candidate pass.

## Four focused checks

- **Concurrency and outcomes.** Enumerate each branch's positive, negative,
  returned-unavailable and no-response cases. Check how each reaches or waits for
  the join. A returned unavailable result is not a positive result or an absent
  response. Review the joint gate as well as individual arrows; retain native
  fork/join checks rather than bypassing a join to hide a mismatch.
- **Message phases and authority.** Distinguish queued, delivered, acknowledged,
  assessed, authorized and completed. An acknowledgment neither proves completion
  nor proves that completion has not independently occurred. Inspect the target
  function and terminal state, not just a reassuring arrow label. Clock origins
  and decision owners must come from the source.
- **Boundary exchanges.** Inventory each request, response, notification and
  acknowledgment crossing the system boundary, with sender, receiver, payload,
  case identity and source locator. Compare the inventory against context
  interfaces and behavioral scenarios. Coverage of a source paragraph does not
  establish coverage of every message in that paragraph.
- **Revision identity.** Compare prior and new sources, recipe IDs, bindings,
  qualified names and answers. Retain IDs for unchanged concepts; distinguish
  added, changed and removed concepts. Renaming a label can change a native
  qualified name. Session UUIDs are not persistent cross-run identities.

For each check, record source locators, the expected distinction, candidate
model/recipe references, a verdict and rationale. Keep unresolved discrepancies
out of delivered claims until corrected or explicitly identified as unknown.
Review records stay outside the audience-facing visuals.

## Executable review receipt

`scripts/review_source_interpretation.py` checks the freshness and completeness of
an independent review record and its explicit JSON-pointer expectations against
the authored recipe. It does not understand prose or prove that the review is
correct. Use it alongside, not instead of, native qualification and source review.

This executable gate applies to recipe-based authoring. For an existing native
`.sysml` model with view recipes, retain the same source/model/view review as
evidence; do not fabricate an architecture recipe solely to run this checker.

The test fixture in `tests/fixtures/source-review/` illustrates the receipt. Each
focus must be supported with assertions or marked not-applicable with a rationale.
Use `equals` for an exact expected field and `containsIds` for required boundary
messages. Source locators must occur in the source; both source and recipe byte
hashes must match. Record verdicts only after inspecting the source and candidate.

```sh
python3 scripts/review_source_interpretation.py \
  --source SOURCE.md --recipe architecture.json --review source-review.json
```

After any source or recipe change, the old receipt is stale. Repeat the affected
source review, update its evidence and rerun the checks before regenerating or
sharing answers. On revisions, review changed answers as well as model structure.
