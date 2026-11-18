# MBSE view catalogue

Choose a view by the question the reader needs to answer. Record its audience,
system boundary, level of abstraction, model revision, selected element and
relationship IDs, and one check the reader can perform. Keep related views on
the same model revision. Use full names in headings and stable IDs in the
inspector, index or trace table.

The ordinary visual is a communication projection. A SysML view usage exposes
the relevant model elements and may select a standard view definition. A
SysON representation is the populated, saved diagram or table in that project.
Verify those three deliverables independently when each is requested.

The [representation-route companion](../../../../../../resources/tools/unified-visuals/mbse-catalogue/METHOD.md) makes these same 14 families machine-readable and selects a delivery combination by objective, audience, editability, interaction, destination and available tools. Its source is `catalogue.json` beside that method; it carries required facts, acceptance checks, references and separate documented, reported and untested tool claims. Keep family IDs and meanings aligned when changing either record. A viewpoint is the reader's concern; text, native tooling, draw.io, SVG and a playable scene are different delivery routes for selected content.

| View and audience question | Ordinary visual and intended message | SysML v2 model and view | SysON delivery and acceptance |
|---|---|---|---|
| Operational capability map. What must the operation be able to accomplish and who participates? | Group outcomes by mission or operating context. Show supported participation and name the dependency or handoff when drawing one. | Actor/part usages, operational activities and outcome-oriented use cases when their semantics fit. Use an exposed General View or a project-specific viewpoint. | General View or a model-backed projection. Reopen and trace one capability to actors and contributing activities. |
| Operational context. What crosses the system boundary and who retains authority? | Draw the boundary, external participants and typed directional exchanges. | System and external part usages, ports, interfaces and flows. General or Interconnection View as appropriate. | Scoped Interconnection View. Check both endpoint occurrences, direction where modeled, and payload. |
| Operational architecture. How do participants cooperate? | Place activities inside participant regions and draw named exchanges between them. | Actor usages, performed actions, item flows or messages. Use a concern-specific projection where standard rendering lacks the combined form. | Verify actor-to-action identity and returned exchanges. Prefer a checked projection if participation and exchanges cannot be shown together. |
| Decomposition. What makes up this responsibility or function? | Tree, explicit nesting or parent/child table. | Composite part/action usages and their actual ownership. General View or a tree/browser presentation. | Show the named parent and its immediate children. Inventory rows alone cannot demonstrate hierarchy. |
| Functional dataflow. What does each function consume and produce? | Connect function inputs and outputs with labeled payload arrows. | Typed action parameters and flow usages with resolved source and target. Action Flow or concern-specific view. | Verify the flow edges. The supplied exercise reported ports/parameters without functional-flow edges in a generic action view; re-test the selected representation and version. |
| Logical architecture. Which responsibilities are allocated the functions and what passes between them? | Capella-style structure with allocated functions inside responsibility boundaries. Label crossing exchanges and distinguish them from control sequence. | Part usages, allocated action usages and typed exchanges. Expose the exact usages and relationships. Use performed usages only when the model asserts performance. | Checked combined projection plus native focused views when needed. Select an exchange and confirm both function usages, their explicit allocations and direction. |
| Interconnection. Which interfaces connect exact occurrences? | Port-to-port wiring and a short interface register for payloads or authority. | Part usages, compatible ports, connection/interface usages, typing and item flows. Interconnection View. | The supplied exercise reported native port-to-port connections. Check each exact port and owner; place labels so adjacent wires remain distinct. A connector alone does not establish a payload transfer. |
| Allocation. To which responsibility is the function usage assigned? | Function-to-part arrows or a matrix; include the scenario-to-function link where a reader starts at a step. | Allocate the exact function occurrence to the part occurrence. Keep definition, use, performance and role distinct. | The supplied exercise reported scoped allocations. Related Elements sometimes showed anonymous Feature endpoints; offer readable navigation to the exact function and part. Grouping does not change their semantic ownership. |
| Scenario sequence. Which participant sends what, and in what order? | Lifelines and named messages for one case, optionally with alternatives. | Occurrences, messages/transfers and ordering, with Sequence View when supported. | Validate actual renderer on the installed version. Use a sequence diagram or ordered interaction table if unavailable. |
| Action flow. What happens on success, rejection, retry or concurrent work? | Activity diagram with guards and explicit entry and exits. | Action usages, successions, typed flows where needed, decisions/fork/join as applicable. Action Flow View. | Import, populate and save. Replay the positive and exception paths using the visible edges. Confirm concurrency and completion independently where present. |
| Lifecycle. When does a subject change state? | States and triggered, guarded transitions. | State definition, state usage or exhibited state on its subject, transitions with triggers and guards. State Transition View. | Distinguish state IDs from readable state names. Check initial state display and a return or failure branch. |
| Requirements and V&V. What must hold and how is it checked? | Register, traceability matrix or focused requirement graph. | Requirement usages, subjects, assumptions/criteria, derivation and verification cases where supported. Use an exposed General View or table/matrix projection. | Requirements Table View in SysON is tool-specific. Reopen with rows populated; check IDs/titles/statements and trace one subject and planned check. |
| Physical realization and deployment. What implements the logical design, and where? | Physical breakdown, deployment map, interface drawing or as-built overlay. | Physical part usages, connections and explicit realization/allocation across layers. General or Interconnection View. | Validate scope and actual deployment evidence. Keep options visible when equipment or locations remain undecided. |
| Trade, assurance or risk. Why select this option and what evidence supports the claim? | Trade table, decision record, assurance argument or causal diagram matched to the question. | Analysis cases, constraints, measures and traces when their meaning is established; preserve evidence authority. | Validate the chosen representation separately from SysML identity. A model assertion or a planned check alone supplies no evidence of performance. |

## Publish a view

The exact standard view definition identifiers in SysML 2.0 Part 1 §9.2.20 are `ActionFlowView`, `BrowserView`, `GeneralView`, `GeometryView`, `GridView`, `InterconnectionView`, `SequenceView` and `StateTransitionView`. `GridView` covers table/matrix presentation families; `TabularView` and `RelationshipMatrixView` are not additional definitions in that package. SysON representation names and their support must be recorded separately. Selecting a standard definition does not establish that a renderer supports it.

1. Write one question and one checkable reader task. Select exact occurrences
   and semantic edges, including external participants and open authority where
   they matter. Name the view for the outcome or decision.
2. Build the simplest representation that preserves that meaning. Use a
   component boundary to show allocation, endpoint labels to show transfer,
   and a separate action or sequence view for order. Preserve unknowns in the
   diagram or immediately beside the affected relation.
3. Qualify the source, compare the exposed graph with independently stated
   facts, then inspect the rendered labels, arrowheads, scopes and link targets.
4. In SysON, populate the saved representation and reopen its direct link in a
   fresh session or after reload. Inspect endpoints and representative branches
   at the intended size. If the tool cannot render the relation, use a named
   checked projection for it and link the relevant native model context.

When an edge is missing, isolate the failure before editing: confirm the edge
exists in source, its end references survive import, the view exposes all
needed elements, and the renderer supports that pattern. A border glyph on
an action can be a directed parameter rather than a structural port; check
the actual metaclass, owner, direction and type. Native names or tool IDs
can change on textual reimport. Reconcile against the project's stable IDs.

Only claim the view families, tool versions and representative cases actually
verified. Diagram appearance, source semantics and engineering acceptance each
need their own evidence.

Sources: [OMG SysML 2.0, §§7.26, 8.2.3, 9.2.20](https://www.omg.org/spec/SysML/2.0/Language/PDF),
[ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html),
[Eclipse Capella diagram families](https://mbse-capella.org/features.html),
[NASA systems engineering handbook](https://www.nasa.gov/reference/system-engineering-handbook-appendix/),
and [SysON Interconnection View](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/features/interconnection-view.html).
