# Communicate a SysML model through selected views

Use the diagram reader as a communication layer over the same qualified semantic facts used by the SysML lab and agent queries. The model and its source revision own meaning. Rendering does not discover model facts or validate SysML. This local route does not modify or release the separate modeling product.

## One model, one selector

`sysml-reader` connects existing qualified semantic view recipes to one standalone interactive reader. It uses native Architecture, Tree, Lifecycle and Dataflow diagrams, plus custom semantic diagrams, matrices and a membership browser in the same visual language. The [view-family mapping](SYSML-VIEW-MAP.md) and [machine-readable registry](sysml-view-map.json) define one primary route for each of the eight standard families and distinguish implemented profiles from planned work.

```sh
python3 scripts/archify.py sysml-reader \
  --source /model/model.sysml --report /evidence/qualification/report.json \
  --views /model/views.json --output /review/system-reader --title "System model"
```

Use the same view recipes supplied to qualification. Every recipe is bound to its exact managed report and source revision. The pump fixture demonstrates eight qualified recipes and two derived interface matrices; the matrices reuse the interface facts, rather than asserting a separately qualified model view. A changed source requires fresh qualification and regeneration. Invalid or mixed revisions leave the last good export intact. `--replace` only replaces an output directory carrying this adapter's reader marker; inputs cannot be inside it.

The exported folder includes `index.html`, `model.sysml`, `views.json`, `reader.json` and license notices. The HTML is self-contained. The selector retains shared component selection across relevant views, distinguishes repeated component occurrences, and provides optional exact source inspection. IDs, hashes, renderer names and receipts stay in the sidecar. State conditions remain readable below the diagram; model declarations do not become executed verification results.

The port renderer reuses the specialist's qualified endpoint resolver and geometry, with an explicit modern card treatment. Contact and same-value binding lines are undirected. Only exported item flows carry arrows. The matrix represents contacts/bindings symmetrically and flows in their declared direction, retaining multiple relations and source witnesses per cell. Empty cells mean no represented relationship in the selected scope. Collections and unsupported endpoint profiles remain disclosed in the scope details and sidecar.

Native automated checks apply before the semantic binding and direction adaptations. Additional identity/endpoint checks cover the composed reader; this is not a claim that the native artifact checker qualifies custom diagrams or the final multi-view wrapper. Inspect the assembled output in `iab`, including cross-view selection, source inspection, a matrix flow, behavior conditions, narrow layout and the needed export.

## Standalone behavior ownership route

`sysml-hierarchy` calls the specialist's managed `explain` command, which verifies the complete managed report against the supplied model. The adapter checks that returned source/report identities and target match, then maps the declared state/action ownership tree into the native Tree renderer:

```sh
python3 scripts/archify.py sysml-hierarchy \
  --source /model/model.sysml --report /evidence/qualification/report.json \
  --target 'System::operatingBehavior' --output /review/behavior-hierarchy.html
```

Use `--replace` only for an intentional regeneration. The output retains editable diagram JSON, the normal delivery/review receipts, and `behavior-hierarchy.model.json` with the complete typed projection, exact model evidence, source/report identities and node mapping. Those files preserve traceability without printing raw IDs, hashes or backend records in the reader. Preserve the original model and complete qualification directory separately. Stable view IDs are derived from the report's element identities; stability across separate Pilot sessions is not promised.

The view preserves distinct same-name elements, exact names, ownership, typed entry/action boundaries, concurrent-region declarations and unknown parallelism. It draws containment only. Transitions, flows, triggers, guards, effects, obligations, timing and satisfaction are **not drawn**; the subtitle discloses that scope. The complete specialist projection retains its supported relationships, conditions, source anchors, warnings and limits in the model sidecar. Partial coverage stays visible in the page. Unknown, stale, unmanaged, invalid or unsupported selections are refused rather than parsed from source text or diagram labels.

Inspect the result in `iab`, including Finder, node selection and tree collapse. A readable hierarchy can help a stakeholder navigate behavior ownership; it does not explain how the system changes state. Use the existing [source-bound behavior explanation](../../methods/html-explanation/README.md#automatic-model-explanation) or the specialist's concern-specific behavior view when conditions and transitions answer the question.

## Coverage boundary

See the maintained [eight-family mapping](SYSML-VIEW-MAP.md). The [expanded design study](examples/pump-station-study/README.md) demonstrates 25 presentations across all nineteen atlas purposes. Dedicated typed projections add actions/parameters, concurrent state regions, message events, membership, allocations, constraints, analyses, variants, box geometry and declared timing. Each profile remains bounded by the registry; unsupported shapes, expression operations, control subtypes or unresolved facts are refused. Native renderer availability alone is not semantic extraction support.

## Semantic selection recipes

A recipe with `renderer: "semantic"` and `readerProfile` asks the reference harness to resolve and bind the exact model selection without invoking its SVG renderer. The managed report carries `semanticFieldsVersion: 2`, source/recipe receipts and typed fields for memberships, variants, values, expressions and message events. `semantic-selection-bound` qualifies that selection, not the custom SVG. The Python projections consume those facts; diagram layout never supplies semantics. The reader rejects stale source/recipes and unregistered profiles before publishing an export.

Build the expanded sample using the same `sysml.py qualify` then `archify.py sysml-reader` route above, with `examples/pump-station-study/model.sysml` and its adjacent `views.json`. HTML is self-contained; the export also includes the original model, recipes, separate license notices. No donor branding or engine working logs appear in the presentation.
