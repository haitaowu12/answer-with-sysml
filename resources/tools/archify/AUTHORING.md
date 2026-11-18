# Author an explorable engineering explanation

Start with the audience, review question, evidence and boundary already supplied. State what the diagram must let the reader find or trace. Select the view by that task; do not start by filling a template with convenient source filenames. This adapts Archify's pinned [authoring defaults](upstream/references/authoring-defaults.md) and [repository authoring](upstream/references/repository-authoring.md). Read the relevant source sections and exact schema before writing, using the local commands below. Examples teach structure, not project facts.

Apply the [subject-led reader policy](READER-POLICY.md): use the subject's title and meaningful labels, with no renderer promotion or backend working notes. Keep source inspection available on demand and material limitations visible. For model-backed work, use the [SysML projection contract](SYSML.md). The newer upstream description-first and source-backed examples reinforce focused questions and distinct alternatives: mutually exclusive scenarios must not become consecutive steps in one sequence.

## Choose the semantic type

| Type | Reader question | Example under `upstream/examples/` |
|---|---|---|
| `architecture` | What components interact, and across which boundaries? | `web-app.architecture.json` |
| `workflow` | What happens next, including decisions and returns? | `agent-tool-call.workflow.json` |
| `sequence` | Who sends what to whom, in which order? | `cache-miss-request.sequence.json` |
| `dataflow` | Which values are consumed, transformed, stored and delivered? | `product-analytics.dataflow.json` |
| `lifecycle` | Which transitions change state, including recovery? | `deployment-release.lifecycle.json` |
| `erd` | What tables, attributes, keys and cardinalities exist? | `orders.erd.json` |
| `class` | What type contracts and relationships exist? | `payments.class.json` |
| `tree` | What belongs under one parent? | `payment-platform.tree.json` |
| `timeline` | When did supported events happen? | `payment-incident.timeline.json` |
| `waterfall` | Where did recorded elapsed time go, including overlap? | `checkout-request.waterfall.json` |

`python3 scripts/archify.py types` prints exact schema, shared-schema, renderer-reference and example paths. Use `schema TYPE` and `example TYPE`, then read `upstream/schemas/common.schema.json` and the printed reference when fields or semantics are unfamiliar. Architecture uses the shared authoring contract; the other modes have renderer READMEs. `guide "scenario"` helps resolve an ambiguous type. It is not evidence about the subject.

Read the complete selected mode schema rather than guessing keys, enum values, boundary kinds or supported features. Mermaid can supply topology for an agent-authored translation; there is no automatic Mermaid parser. Preserve all meaningful nodes, directions, labels, conditions and multiplicities, and disclose unsupported semantics rather than substituting a visually similar arrow.

## Compose meaning and evidence together

Lead with the main journey or question. Group roles only when doing so preserves control ownership, actual reads/writes, trust/persistence boundaries, exceptions and responsibilities. Put additional explanations in useful cards; a card cannot qualify an otherwise unconditional arrow. Use accurate legends, including non-software terminology when relevant. Neither a node count nor fewer crossings justifies deleting a required fact.

For repository evidence, inspect the actual call/write/transition sites. Pin the credential-free origin and full commit in `meta.repository`, attach exact repository-relative source ranges to the owning nodes, and pass `--repo-root`. The verifier reads committed bytes at that revision. Dirty working-tree content must not be represented as verified `HEAD` evidence. Use a separately committed snapshot when appropriate, or explicitly disclose the uncommitted basis without a verified-repository claim. `link_mode: "local-only"` preserves local Git verification without remote source links; it does not snapshot uncommitted files.

Each node accepts at most three source ranges. Keep additional claim-level evidence in cards or the maintained project record; never drop important support merely to fit the schema. A source badge establishes the existence and bounds of the citation. Check entailment separately: a declared responsibility is not proof of direct I/O, a connection is not necessarily a flow, and a suggested gate is not an approval. Preserve unknown, inferred, proposed and observed status in visible wording.

## Place a readable first candidate

Follow the mode's measured layout and automatic-routing defaults before adding manual routes. Read [native authoring defaults](upstream/references/authoring-defaults.md) for the selected mode. Its composition, branch/store/return/fan-out placement, source fidelity, label spacing and language guidance are adopted. Its `finalize`, updater and output-folder commands are replaced by [the local workflow](README.md#author-and-render).

- Architecture: place connected main-path neighbors together; put a branch/store near its actual owner and returns in a clear corridor. Leave room for full edge labels and real boundary membership. Start automatic routes; add pins only for supplied geometry or a measured defect.
- Workflow and Lifecycle: use the current native schema and compiler layout; preserve decision labels, gates, failure exits and recovery transitions. Do not infer scheduling or parallel semantics from a layout.
- Sequence: budget message-note height, activations and phase boundaries together. Preserve ordering and note meaning. Self-message loops are unsupported; an internal action may be explained in a note beside its surrounding real interaction.
- Dataflow: work backward from outputs to the values their producer consumes. Keep storage distinct from computed in-memory values. Label every flow; dashed/security/emphasis variants must match their actual legend meanings.
- ERD and Class: retain physical columns, key roles, references, cardinalities and selected contracts. Arrange domains and types into readable rows/columns. A conceptual entity map must say it is conceptual. Class relationships retain their distinct UML meanings; these are not SysML v2 notation.
- Tree: one parent per node, no cross-branch dependency edges. Prefer rightward layout for an unbalanced repository or long shallow list; default downward layout suits balanced decompositions. Check actual size rather than accepting empty space and tiny labels.
- Timeline: preserve time zones and uncertainty; explicitly distinguish observed from illustrative events. A date-only entry must not silently become a precise observed time. Automatic compressed gaps must remain disclosed.
- Waterfall: use supported recorded timings to claim `measured`; otherwise declare `illustrative`. Parent durations are inclusive, incomplete spans are lower bounds, and overlapping spans are concurrent intervals. No dependency/critical-path result is inferred.

Retain the user's visual identity and authored language. Built-in style presets, semantic icons, bundled brand marks and locale catalogs are available on demand. Read [brand marks](upstream/references/brand-marks.md) for explicit branding and [viewer features](upstream/references/viewer-runtime.md) for reader capabilities. Existing still/reduced-motion preferences remain valid. Motion illustrates the authored diagram and must not invent execution facts. Do not copy the upstream restrictions that require a user request for every subtitle or visual style; use the task and current design contract.

## Generate, repair and inspect

Write one complete typed candidate. Run `python3 scripts/archify.py render INPUT --output OUTPUT.html` with `--repo-root` for repository evidence. The adapter performs native delivery and strict artifact/provenance checks and retains the normalized editable source. It does not run a browser or silently promote automated checks to visual review. Pre-validation is optional; use `validate` for focused diagnosis.

For a failure, read structured diagnostics and the relevant [authoring contract](upstream/references/authoring-contract.md), [Architecture repair](upstream/references/architecture-layout-repair.md), or [delivery/recovery reference](upstream/references/delivery-contract.md). Repair the connected layout or schema neighborhood in JSON, preserving all semantic facts. Rerender, using `--replace` for an intentional revision. After two focused repairs fail, change the layout approach or report the unsupported constraint; do not delete labels, alter source claims, weaken a gate, or loop through cosmetic variants. Preserve native crash-recovery evidence if reported.

Inspect the actual populated artifact in `iab`, at the intended desktop size and a narrow viewport. Check label readability, endpoints, direction, conditions, legends, source inspection and the relevant interaction. Narrow views may require scrolling and zoom; do not claim mobile usability from containment. Exercise Finder/Route/Reach/Lens for graphs, collapse for trees, or the change navigator for comparisons. Inspect actual requested exports, including complete topology after a collapsed view. Keep essential limitations visible without opening metadata.

For comparison, run `python3 scripts/archify.py compare BASE.json HEAD.json --output DELTA.html`. Use stable authored IDs and inspect the Before/Delta/After views and exact changed IDs. Movement, label changes, topology, evidence and boundary changes retain their separate classifications. This is an authored-input comparison, not discovered runtime impact or an engineering approval.

Deliver the HTML and editable source with a concise takeaway and material limitations. State automated, browser/perceptual and export evidence separately. Do not expose the production bookkeeping as the reader's main flow. Do not claim universal superiority: choose Archify for its interactive diagram strengths, and the existing narrative or formal-model route where it answers the task better.


## Reading-size preset for architecture views

For mixed-stakeholder reading, add `"reader_typography": "readable-v1"` inside architecture `meta`. This owned extension gives relationship labels a 14px source size and primary node labels a 16px preferred size with a 14px fitting floor. Omission keeps the retained native sizes. Other diagram types do not accept this field.

The renderer uses the same sizes for text, label masks, router obstacles and minimum node-width diagnostics. Widen a rejected node or shorten its wording without changing the meaning; do not hide an overflow with CSS. The direct HTML reader preserves source width with contained horizontal scrolling. Embedded views can scale. Supporting sublabels, legends and UI text retain their existing sizes, so this is not a claim that every character is 14px.

The [same-brief comparison](../../output-catalogue/examples/archify-comparison/index.html) retains the pristine donor, owned baseline and repaired reader. Both baseline variants passed the automated gate with 8px relationship text. Passing that gate alone is not reading-size acceptance. Inspect the initial viewport, selected relationships, narrow-screen scroll and requested export before delivery.
