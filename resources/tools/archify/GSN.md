# GSN assurance visualization

Reviewed 2026-10-16. GSN provides argument semantics distinct from SysML model semantics. Reuse the adopted reader's styling and navigation while retaining GSN symbols and typed relationships. Do not encode an assurance case as an ordinary Architecture or single-parent Tree diagram.

The [SCSC standard page](https://scsc.uk/gsn-standard), checked through the in-app browser, identifies Version 3 as current. The [retained standard](../../../sources/standards/04_OTHER/GSN_Community_Standard_v3/Source_Records/full-text.md) supplies the detailed authority: Part 1 §1:2, especially PDF pp.17–19. The original figures on pp.17–18 were also inspected. [The maintained interpretation](../../../knowledge/standards/04_OTHER/GSN_Community_Standard_v3/GSN_Cheat_Sheet.md) addresses argument/evidence review beyond graphical structure.

| Meaning | Required rendering | Current core reader |
| --- | --- | --- |
| Goal | Rectangle; claim | Implemented |
| Strategy | Parallelogram; inference approach | Implemented |
| Solution | Circle; evidence reference | Implemented |
| Context | Rounded-ended context shape | Implemented |
| Assumption | Oval with A | Implemented |
| Justification | Oval with J | Implemented |
| Undeveloped goal | Goal with hollow diamond below | Implemented from the retained `undeveloped_goal` representation |
| SupportedBy | Solid arrowhead toward supporting element | Implemented; goal→goal/strategy/solution and strategy→goal |
| InContextOf | Hollow arrowhead toward contextual element | Implemented; goal/strategy→context/assumption/justification |
| Shared support | Directed acyclic graph, allowing multiple parents | Preserved; not reduced to a single-parent tree |
| Modules/away elements, patterns, confidence and dialectic extensions | Extension-specific symbols and meaning | Require separate profiles; unsupported node/link types are refused |

Structural validity cannot establish claim truth, argument sufficiency or evidence acceptance. A planned test is not completed evidence. An undeveloped branch remains visible even when other branches have evidence references. The core reader does not add pass colors or close findings from connectivity.

## Existing assurance-workbench integration

The retained [GSN v3 draft profile](../../methods/compliance-assurance/compliance-assurance-skill/references/gsn_v3_profile.md), [assurance-case schema](../../methods/compliance-assurance/compliance-assurance-skill/schemas/assurance_case.schema.json) and exporter already provide typed nodes and relationships. `scripts/gsn_reader.py` consumes that JSON shape for the supported core subset and keeps every node/edge identity and the original source JSON. It deliberately rejects legacy `decomposes`, `argued_by`, `challenges` and other non-core links instead of silently restyling them as support.

The current notebook method keeps governed obligations, claims, evidence assessments, findings and reviewer dispositions authoritative. The derived GSN projection remains a view. A graphical editor must send edits to those upstream records or retain explicit proposed changes; changing a generated JSON view is not sufficient write-back. See [the graphical-editing assessment](GRAPHICAL-EDITING.md).

## Demonstration and command

The [pump-station argument](examples/pump-station-assurance/assurance-case.json) is an eight-node, seven-relationship draft illustration tied to the existing SysML design study. Its design count branch cites declarations of 2 installed against a minimum of 2; its installed-performance branch is explicitly undeveloped. The top claim is proposed, not established. GSN does not become SysML merely because it references that model.

```sh
python3 scripts/archify.py gsn-reader \
  --source resources/tools/archify/examples/pump-station-assurance/assurance-case.json \
  --output /path/to/Pump-Station-Assurance-Reader \
  --title 'Pump station · Assurance argument'
```

Use `--replace` only to deliberately replace an owned GSN reader export. The builder preserves the last good output if validation/rendering fails, rejects duplicate IDs, missing endpoints, disallowed type pairs and cycles, and retains the source argument unchanged. Evidence references are displayed on demand; the reader does not automatically open or copy their paths. When transferring the example, include the original `examples/pump-station-study/model.sysml` as `model.sysml` beside the HTML, as the packaged demonstration does.

The delivered folder includes self-contained `index.html`, the argument JSON, reader facts and separate license notices. No branding, engine working text or acceptance receipts are placed in the reading flow. Full statements, declared statuses and evidence locators open on selection. Native renderer artifact checks are not claimed to qualify this custom GSN SVG; its mapping tests and actual browser inspection are separate evidence. No graphical editing has been implemented by this command.

