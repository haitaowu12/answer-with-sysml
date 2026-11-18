# SysML v2 meaning → diagram presentation

The [standards-led MBSE atlas](MBSE-VIEW-ATLAS.md) supplies the nineteen engineering purposes. [sysml-view-map.json](sysml-view-map.json) is the route registry and detailed support boundary. This mapping follows OMG SysML 2.0 Part 1 formal/26-03-02, especially §7.26, §8.2.3 and §9.2.20. Rendering families are broader than individual MBSE concerns; a concern can require several related presentations.

| Standard family | Native visual reuse | Current primary implementation | Demonstrated bounds |
| --- | --- | --- | --- |
| GeneralView | Architecture, Tree, Class primitives | Native summaries and custom typed graphs | Concerns/viewpoints, use cases, direct usage/typing, occurrence breakdown, requirements and declared variants/selections |
| InterconnectionView | Architecture and Dataflow | Custom ports and parameter networks; native exchange summary | Direct binary part.port connections; exact input bindings and selected constraints |
| ActionFlowView | Workflow styling | Custom action/control/parameter renderer | Local actions, fork/join, control versus item flow, direction-bearing parameters; no general loops or performer lanes |
| StateTransitionView | Lifecycle for flat states | Native flat graph plus custom hierarchical regions | Source-owned nested/concurrent states, declared entry, trigger/guard/effect and entry/do/exit inspection |
| SequenceView | Sequence styling | Custom event/lifeline renderer | Explicit message endpoints, self-messages and acyclic local event precedence; no inferred timing or arbitrary nested interactions |
| GeometryView | No native equivalent | Custom isometric envelopes | Positive declared rectangular boxes in supported units; no invented assembly placement or transforms |
| GridView | No native matrix equivalent | Rectangular matrices and bounded analysis/timing presentations | Interfaces, allocations, planned verification coverage, scalar analysis comparisons and explicit timing budgets |
| BrowserView | Tree interaction idea | Custom searchable indented membership browser | Source-owned namespace membership; separate from occurrence decomposition and imported library expansion |

The [single model study](examples/pump-station-study/README.md) yields 25 presentations. Exact managed source and recipe receipts bind every view; all visible model nodes and relationships retain source witnesses. Selection and source inspection share one reader. Renderer names, IDs, hashes, compiler output and working notes stay outside the reading flow. Separate license notices retain attribution without presentation branding.

Native candidates are reuse assessments, not equivalence or conformance claims. Workflow cannot replace all v2 action semantics, Class/ERD cannot replace v2 definition/usage semantics, and Timeline/Waterfall cannot establish timing from graph order. Custom profiles refuse unsupported facts instead of manufacturing plausible diagrams. These styled communication views do not claim complete SysML v2 graphical-notation conformance or full language coverage. They do not change or release the separate modeling product.
