# SysML v2 element authoring procedures

Work in a separate candidate based on a named source revision. For each item
record the source or derivation, stable ID, intended level, owning namespace
and one fact the reader must be able to verify. Keep the package layout
predictable. Place reusable types in Types; roles and operational activities
in Operational; functions and their exchanges in System; candidate parts,
allocations and contracts in Logical or explicit boundary packages; behavior
in Scenarios or lifecycle definitions; obligations and checks in Requirements
and Verification; decisions and presentation scopes in their own packages.
Keep scope-specific views close to their subjects when that helps discovery.

| Element | Procedure | Inspect before accepting |
|---|---|---|
| Stakeholder, actor, capability | Identify the external or internal role, authority and operational outcome. Record actor participation and actual contributing activity. Map an operational capability to SysML use cases only when actor/subject and scenario semantics fit. | A capability has an outcome and meaningful participants or activities. The declared boundary leaves external authority visible. |
| Definition and usage | Define the reusable classifier and its features. Create separate contextual usages with names, ownership and types. Retain stable identities across renames. | A reader can distinguish the type from each actual occurrence, including repeat uses. |
| Part, action and performance | Name the role or part for its responsibility and the action with a verb and object. Model data in or out and context. Use perform for an asserted performance relationship. Keep lifecycle exhibit usages attached to their subjects. | A scenario step is distinct from its type and matching system function. Check the actual performance or allocation relation and the exact endpoint usage. |
| Port, interface, connector | Specify what each endpoint offers or consumes, item type, direction, multiplicity and applicable conditions. Connect occurrence-owned or inherited ports through resolved paths. | Both endpoint owners and port usages resolve. Port compatibility and payload meaning agree. A connector alone states structure. Explicit flow supplies transfer semantics. |
| Flow, succession, message | Use item-bearing flows for transfer, successions for ordering, and messages for interaction between participants. Introduce branches with readable applicability and show recovery and completion explicitly. | Source and target are exact endpoints. Timing, concurrency and inferred semantics remain within the actual model. |
| State and transition | Start from a named lifecycle subject and initial state. Name states as conditions, events as triggers, guards as conditions and effects as actions. Separate restored readiness from approval to resume when evidence distinguishes them. | Trace entry, normal and exception transitions, and any terminal or ongoing states while preserving unresolved criteria. |
| Allocation | Identify the function occurrence and logical responsibility, document why, then model the relation. Add a physical or organizational realization only when supported or explicitly proposed. Record the role named by a scenario separately. | Follow step → system function → allocation → logical part. Then identify the distinct evidence for any role or real-world implementation. |
| Requirement and verification | Use the stable Req Id as declared short name, a readable declared name, and a standalone obligation in Documentation. Bind its actual subject, preserve criteria and supplied quantities, and retain rationale/source in a separate comment. Link a planned case with method, setup and expected outcome. | Check the actual register columns, subject, applicable condition and verification target. Preserve the distinction between a planned check, its result and accountable acceptance. |
| Decision, risk and evidence | Record options, decision owner when known, affected IDs, source anchors and evidence required to close. Preserve uncertain values and design proposals. | A reader can see what is known, proposed or open and locate the source without searching duplicated documents. |
| View and representation | Specify the question and the selected scope with the [view catalogue](view-catalogue.md). Use the same identities in ordinary visuals, SysML and SysON. Save the rendered view and a direct entry point. | Confirm the saved diagram survives reload; check exact endpoints, readable labels and an actual reader journey. |

Use the [validated syntax](validated-syntax.md) and locked runtime for new
constructs. Qualify the model and independently check representative native
facts before relying on a generated view. When a new render target is
requested, check its import and saved presentation separately.

The airport exercise exposed a useful boundary: a source may assign a person
to set a route while leaving confirmation authority and admission prevention
open. The model can propose a logical owner and guards while retaining those
decisions explicitly. Record the setter, confirmation authority, admission
authority, hold mechanism and feedback separately when each affects the review. Grouping functions in a diagram does not establish
ownership unless the grouping is derived from actual allocations.
