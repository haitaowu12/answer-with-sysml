# Requirements and architecture views

## Record the obligation

Use one stable requirement ID as the SysML declared short name and a concise
human title as the declared name. For new architecture recipes, write a
standalone `statement` with the responsible subject, applicability and
observable obligation. Use “shall” for an obligation. Capture one reviewable
obligation per requirement and flag independently testable obligations for
controlled decomposition when baselined identifiers would change. Keep original
units, thresholds and measurement conditions. Record open inputs explicitly.

| SysML element | Content |
|---|---|
| Declared short name / Req Id | Stable identifier from the controlled record |
| Declared name | Meaningful title, unique within the namespace |
| Documentation | Requirement statement only |
| Subject parameter | The affected model occurrence, typed and bound |
| Assumed/required constraints | Actual applicability predicates and criteria when formalized. Use a documented qualitative criterion when the evidence supports only text. |
| Comment | Source locator, rationale, basis, status and applicable decision context. Use a named owned comment so it can be located in Explorer or exported. |
| Verification case | A linked planned check, with method, setup and expected outcome. Keep results and acceptance as separate evidence. |

Preserve the stable ID when improving a title or wording. Reconcile references
after renaming. Add derivation or satisfaction relationships only where their
meaning is supported. A subject binding identifies the object of the obligation.
A planned verification case identifies how the team intends to check it. In
SysON, inspect the displayed Req Id, name and statement after import, then open
the owned comment and follow one verification target. See [OMG SysML 2.0 Part 1,
§7.21.2](https://www.omg.org/spec/SysML/2.0/Language/PDF) and the [NASA Systems
Engineering Handbook, §4.2 and Appendix C](https://www.nasa.gov/reference/4-0-system-design-processes/).

## Choose the view from the review question

Identify the stakeholder, decision, model scope and the relationships that
answer the question before choosing the notation. Specify what the reader
should be able to trace from one named occurrence to another. Review the
populated representation alongside its source scope.

| Question | View | What the reader must be able to follow |
|---|---|---|
| What is inside the system and who interacts across its boundary? | Operational context | System boundary, external actors or services, named exchanges, and responsibility or decision authority |
| What is the system made of or how is a function broken down? | Decomposition | Parent and children, with containment, nesting or a tree that makes the hierarchy explicit |
| Which responsibility performs a function? | Allocation | Exact function occurrences, responsible parts and allocation relationships. Use a matrix when that answers the question more clearly. |
| How are responsibilities connected? | Interconnection | Usage occurrences, their ports, and the model connector or interface between the exact endpoints. Label the payload and identify direction where modeled. |
| What happens for this case? | Action Flow | Entry and exit, named action occurrences, successions, explicit guards, retries, failure paths and concurrent contributions as applicable. Distinguish typed transfers from control succession. |
| When does the subject change mode? | State Transition | The lifecycle subject, initial state, trigger, guard, transition outcome and any terminal state |
| What obligation applies and how is it planned to be checked? | Requirements and verification | Stable IDs, subjects and trace links from requirements to planned cases and evidence |

A native view declaration defines a scope. The SysON diagram must separately
show the relationships and their endpoints. Check the saved representation
after reopening it. A collection of unconnected elements can serve as an
inventory. Use a relationship table or a qualified model-backed projection
when the target tool cannot show the required connectors. Label that surface
for what it shows and keep a direct link to the corresponding native view or
model element. See [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html),
[OMG SysML 2.0 Part 1, §7.26](https://www.omg.org/spec/SysML/2.0/Language/PDF),
and the SysON [Interconnection](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/features/interconnection-view.html)
and [Action Flow](https://doc.mbse-syson.org/syson/v2026.11.0/user-manual/features/action-flow-view.html) documentation.

For an existing SysON 2026.11.0 model, populate a focused General View for
allocation with the exact functions and responsible part. For a focused
Interconnection View, add both part usages and the existing interface
usage, including its endpoint ports. Use the normal diagram tools or the
equivalent GraphQL `dropOnDiagram` operation. Read back the saved diagram
and match each required edge to the intended semantic relationship and
source/target occurrences. For a port connection, check the ports and their
owning occurrences. Add a payload label or a nearby contract key where the
tool displays only the connector ID. A successful add or layout operation
alone is insufficient: a view can contain all the requested nodes and still
omit every required relationship.
