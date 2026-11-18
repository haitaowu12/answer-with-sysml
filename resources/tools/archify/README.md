# Interactive visual explanations

The [unified visualization reader](../unified-visuals/README.md) provides Technical/Editorial profiles over this complete native runtime, selected supplemental Diagram Design families, composed explanations and editable exports. Start there for profile-driven technical/editorial output; this package remains the underlying native schema, adapter and Architecture Delta owner. Current engineering/modeling project outputs retain their source contracts.

Use this native engine beneath the default unified reader when readers need to explore a system, follow authored paths, inspect sources or collapse a hierarchy; use its direct comparison adapter for architecture changes. The bundled ten-type renderer produces editable JSON and standalone HTML with inline SVG. It works through [the local adapter](../../../scripts/archify.py), without a separate skill installation or npm dependencies. Requires Python 3.10+ and Node.js 18+.

`development-workflow` owns the adapter and presentation. `knowledge-engine` owns evidence and engineering meaning; the SysML specialist retains model semantics and qualification. Read [AUTHORING.md](AUTHORING.md) before a fresh diagram. The native [schemas](upstream/schemas/README.md), examples and renderer references supply exact syntax. Upstream [SKILL.md](upstream/SKILL.md) is retained source material, not an installed owner or a second workflow.

Delivered pages use the subject's identity. The [reader policy](READER-POLICY.md) removes donor promotion, decorative revision stamps, raw node IDs and generic renderer metadata from reader controls, while retaining useful sources and relationships. Keep production receipts beside the output rather than displaying backend working notes. Existing HTML must be regenerated for these changes to apply.

## Choose by reader task

| Task | Preferred route |
|---|---|
| Explorable architecture, process, interaction, lineage, state, schema, class contract or hierarchy | Archify; pick the matching type in the authoring guide |
| Recorded chronology or request/agent execution timings | Archify Timeline or Waterfall, with supported dates/timings and explicit evidence status |
| Review authored Architecture changes | Archify exact-ID Before / Delta / After comparison |
| A small static relationship that is clear inline | Mermaid through the existing visual-explanation method |
| A publication-ready static figure, service blueprint or editorial redraw | [Unified reader](../unified-visuals/README.md) with the selected [Diagram Design guide](../../methods/diagram-design/README.md); preserve source facts and an import fidelity ledger |
| An answer-led page with prose, alternatives, conditions and several different information shapes | [Source-bound HTML composition](../../methods/html-explanation/README.md) around unified-reader views |
| SysML engineering model or formal behavior | [SysML specialist](../../../.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/SKILL.md); any Archify view is a derived communication view, with supported semantics and omissions retained |
| Quantitative charts, dashboards, native slides or video production | Existing format/domain workflow; a diagram renderer does not replace it |

The [standards-led MBSE view atlas](MBSE-VIEW-ATLAS.md) organizes nineteen engineering-purpose profiles under SysML v2 semantics. The [SysML reader](SYSML.md) demonstrates all nineteen purposes through 25 coordinated presentations from [one design-study model](examples/pump-station-study/README.md), with one grouped selector and source inspection. Native styling is shared with custom actions, parallel states, scenarios, matrices, membership, geometry and analysis views. The [eight-family mapping](SYSML-VIEW-MAP.md) and structured registry record the precise limits. These communication views do not claim full graphical-notation conformance.

The [GSN core reader](GSN.md) adds the six core assurance-argument symbols, undeveloped goals and distinct support/context arrows using the same reader styling. The [graphical-editing assessment](GRAPHICAL-EDITING.md) separates view layout from source-model edits and recommends reusing the existing React Flow foundation with domain-specific commands. The static reader retains its read-only model contract. The optional [revisioned model workshop](MODEL-EDITING.md) adds service-backed rename and numeric-value transactions with native source-set export/reopen.

## Author and render

```sh
python3 scripts/archify.py types
python3 scripts/archify.py guide "show calls between an API and its cache"
python3 scripts/archify.py schema sequence
python3 scripts/archify.py example sequence
python3 scripts/archify.py render /project/request.sequence.json --output /project/review/request.html
# For a diagram grounded in a committed repository:
python3 scripts/archify.py render /project/map.json --output /project/review/map.html --repo-root /project/repository
# Revise the editable source, then deliberately replace the previous output:
python3 scripts/archify.py render /project/review/map.source.json --output /project/review/map.html --repo-root /project/repository --replace
python3 scripts/archify.py check /project/review/map.html
# Optional last-good live preview; edit the printed saved source and open its URL in iab:
python3 scripts/archify.py preview /project/map.json --output /project/review/live-map.html
```

Choose an explicit output file. Previews and execution evidence normally belong outside this repository; retained project deliverables use their project location. There is no required `.archify/` folder, timestamp directory or automatic opening. The adapter normalizes only `meta.output` and the selected quality profile. Authored nodes, edges, conditions, evidence and presentation remain unchanged. `showcase` is the default; use `--quality standard` deliberately for dense maps, keeping readability review explicit.

Each render keeps `name.source.json`, native `name.delivery.json` and `name.review.json` beside `name.html`. The editable source is necessary for regeneration. Native delivery and strict artifact/provenance checks must pass; ordinary failed revisions restore the adapter's previous named files. A failed first draft leaves the original candidate available for repair. The wrapper coordinates its own writers and rollback on ordinary errors; it is not a multi-file crash transaction or a guarantee for concurrent native CLI writers. Do not bypass a native crash-recovery diagnostic or delete its recovery files as cleanup.

The review receipt describes automated evidence only. It leaves browser review pending. Inspect the actual result in the Codex in-app browser, check the relevant journey and content, and state which checks actually ran. Do not call it the upstream `finalize` or `browser-check` result: those commands launch separate headless Chrome. The adapter does not invoke them or the donor updater. The retained native commands remain source/runtime facilities, outside the default local workflow.

For a loopback preview, serve the output directory with `python3 -m http.server 8867 --bind 127.0.0.1 --directory /project/review`, then open its HTML in `iab`. Stop the owned server after inspection. Use ordinary file links for delivery; no hosting or upload is implied.

For repeated JSON edits, `preview` starts the native loopback watcher with browser auto-opening disabled. It watches the saved `name.source.json`, retains the last passing artifact on a failed edit and reports its status in the preview shell. The first `name.review.json` records the initial render only; after edits use the current native delivery receipt and `check`, then inspect the refreshed reader. Stop the owned preview with Ctrl-C. This watcher is optional, not a required service for viewing delivered HTML.

## Explore and export

The complete native reader is retained: node Finder, source inspector, direct relationship selection, upstream/downstream authored reach, directed Route Probe, semantic Lens, overview Radar, zoom/reading depth, tree collapse, Presentation Stage, visual presets, locale catalogs and Live/Still controls. Use these when they help answer the reader's question; no custom reimplementation is needed. [Viewer reference](upstream/references/viewer-runtime.md) describes the controls and link state.

Standalone HTML travels with its reader and bundled font. Export supports PNG, JPEG, WebP, light/dark/automatic-theme SVG and WebM; resolved Route/Reach share cards are scoped derivatives. Canonical exports remove transient reader overlays and retain the complete diagram, including collapsed tree descendants. Inspect the actual requested export. JSON and SVG are editable sources; this does not promise native PowerPoint, Visio or drawio objects. External source links still require access to their destination.

Source badges verify Git identity, file existence and line bounds, not whether the cited text entails a claim. Relationships generally have no separate citation field: cite the owning call/write/transition site on its node, and retain additional evidence in cards or the project source record. Authored reach is not runtime impact; animated edges are not execution; an Architecture Delta is not a risk or mergeability assessment. Timeline/Waterfall status labels are authored declarations, so inspect the underlying records before claiming observed/measured values.

## Validation and maintenance

The [28 October revisit](../../../sources/reviews/visual-capability/2026-10-28-styling-revisit.md) reviewed the newer 3.2.0 explainer direction and recommends a separate compatibility pilot. The notebook's shared styling was improved through its own profile/engineering adapters; the retained Archify runtime pin below is unchanged.

```sh
python3 scripts/archify.py doctor
python3 -B -m unittest discover -s tests -p test_archify.py -v
python3 -B -m unittest discover -s tests -p test_sysml_reader.py -v
python3 -B -m unittest discover -s tests -p test_gsn_reader.py -v
python3 scripts/skill_adoption.py resources/tools/archify/skill-adoption.json
./.venv/bin/python -B system/scripts/validate_control_plane.py
./bin/tsb validate
```

The [source record](SOURCE.json), [adoption map](skill-adoption.json) and [evaluation](EVALUATION.md) record the pin, retained mechanisms, host translations and tested scope. `upstream/` contains Archify 3.1.0 at `1c2b42d660e4a7571813fb43839c79e3e9ca7720`, with the documented reader/semantic-hook patches and opt-in readable-v1 architecture typography and omitted generated demo HTML. The 2026-10-16 comparison with upstream `ca67c9f16be0c8cad409cd45190aa052e0649b84` found no production-package changes. New source-backed guides and the pilot evaluation protocol inform authoring and verification; they do not establish measured quality or speed improvement. Keep the [MIT licence](upstream/LICENSE), [third-party notices](upstream/THIRD_PARTY_NOTICES.md) and embedded font notices with redistribution. A refresh compares instructions, runtime, schemas and references, then reruns affected adapter and reader cases. No automatic upgrades or global host configuration changes.
