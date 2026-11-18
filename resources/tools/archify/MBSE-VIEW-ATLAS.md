# SysML v2 semantic views for MBSE

Reviewed 2026-10-16 against **OMG SysML 2.0 Part 1, formal/26-03-02**, not just the local renderer or Pilot implementation. The [retained source and section index](../../models/10_SYSML_V2_LANGUAGE/Source_Records/Source_SysML_v2_Formal_Views_2026-10-16.md) records the evidence. The [formal language PDF](https://www.omg.org/spec/SysML/2.0/Language/PDF) is the normative authority; the [publication page](https://www.omg.org/spec/SysML/2.0) identifies its document version. [mbse-view-profiles.json](mbse-view-profiles.json) holds the structured catalogue.

This is a **SysML v2 semantic catalogue**. It is not the SysML v1 nine-diagram list, a UML substitution, or a catalogue limited by current local extraction. The nineteen engineering-purpose profiles below are our organizing synthesis, not nineteen diagram types mandated by OMG.

## Start from the engineering concern

SysML v2 separates a stakeholder's concern, a viewpoint framing what a satisfactory view must address, a view exposing and filtering the relevant model content, and a rendering producing the artifact. A composite view can combine graphical, textual and tabular subviews. These are model concepts, not merely dashboard tabs (§7.26).

The useful mapping is:

**Engineering concern → SysML v2 elements and relationships → selected standard/custom view definition → primary rendering.**

Assign one primary rendering to each concern-specific profile so the selector stays predictable. Do not force an exclusive one-to-one pairing between all MBSE concerns and eight broad standard families. One concern may need a graph plus a matrix; several concerns may reuse the same family. A shared model identity connects those artifacts.

## The eight standard view families

These are normative standard view definitions (§9.2.20, Table 34), rather than an exhaustive method or engineering deliverable set. Graphical-notation conformance requires the applicable grammar in §8.2.3. A styled communication view can preserve model meaning without claiming that conformance. User-defined views are explicitly permitted (§7.26.5; §8.2.3.1).

| SysML v2 family | What it generally looks like | Semantic content | Correspondence to existing diagram types |
| --- | --- | --- | --- |
| General View | Typed nodes/edges, compartments, nested package or definition/usage views | Exposed model members; typing, specialization, satisfaction, allocation or other selected typed relations | Architecture supplies card/edge styling. Class supplies some visual primitives, but neither is a complete SysML definition/usage renderer. Custom typed symbols and relations are needed. |
| Interconnection View | Nested feature boxes with boundary ports/parameters and connectors | Features, nesting and exact connection endpoints | Architecture supplies containers/cards. Custom endpoint anchoring, port features, bindings and connection/flow distinctions are needed. |
| Action Flow View | Actions, parameters, distinct control/item flows, decisions, fork/join bars, loops and performer lanes | Action performance and coordination, not just a sequence of process steps | Workflow is a partial visual match; custom control/parameter/region support is required for the general v2 case. |
| State Transition View | Rounded states, nested/parallel regions, entry/do/exit compartments and labeled transitions | Trigger, guard, effect and explicit state ownership/concurrency | Lifecycle is a bounded flat-state match. Its default initial/preferred-path cues must not invent model facts. Custom regions are required for richer states. |
| Sequence View | Feature headers, vertical lifelines, event occurrences and horizontal messages; time progresses downward | Event ordering and message endpoints, potentially nested interactions | Sequence is the closest native match. Exported participants, events, message kind and partial ordering must be mapped explicitly; total ordering or duration cannot be inferred. The current native renderer rejects self-messages, so those need a custom extension. |
| Geometry View | 2D/3D spatial shapes, coordinate frames, orientation/projection and optional quantity colors | Spatial items, shape, frames, quantities and transforms | No native match. Develop a spatial renderer from actual geometry semantics. |
| Grid View | Registers, value tables and rectangular relation matrices | Element/value identity and typed row-to-column relationships | No native matrix type. Develop shared table/matrix presentations for allocations, satisfaction, interfaces and verification coverage. |
| Browser View | Indented expandable membership list | Hierarchical model membership from an exposed root | Tree offers collapse/selection primitives, but an occurrence-composition diagram is not this view. Develop the membership browser separately. |

Table 25 (pp.155–156) explicitly illustrates graph, part-tree, nested, table, requirements-satisfaction matrix and allocation-matrix presentations. The representative notation for sequence messages (p.83), action parameters (p.88), performer swimlanes (p.90), requirements (pp.131 onward), and use cases (pp.146 onward) provides concrete visual examples beyond the grammar pages.

## Engineering-purpose catalogue

The family column identifies reusable v2 presentation families. It does not assert that a particular concern is a separately named standard view. Operational, functional, logical and physical are useful method-defined perspectives on the same language; they are not four extra OMG standard families.

| Engineering view / question | SysML v2 semantic basis | Usual visual form | Primary mapping decision |
| --- | --- | --- | --- |
| Stakeholders and concerns: whose question are we answering? | Concern, stakeholder membership, ViewpointDefinition/Usage, ViewDefinition/Usage, satisfaction | Concern–stakeholder–viewpoint–view graph and coverage register | Custom typed concern graph; General/Grid |
| Context: what is inside, outside and crossing the boundary? | Subject part, external parts/actors, ports, connections and explicit flows | Boundary with internal/external features and labeled interfaces | Architecture summary; detailed Interconnection needs custom ports |
| Use cases: what observable value is provided to each actor? | UseCaseDefinition/Usage, subject, actor parameters, objective, include usage | Actor/subject/case relationships and objective compartments | Custom case graph; General, with action/sequence drill-down |
| Scenarios: who interacts in which declared order? | Occurrence/event usages, message/flow usages, successions | Participant lifelines and messages | Custom event Sequence with source ordering and self-messages |
| Model membership: where is this element owned/imported? | Namespace and membership relationships | Indented expandable list | Custom Browser view |
| Definitions and usages: what is reusable and how is it specialized here? | Definition/Usage, feature typing, specialization, subsetting, redefinition | Distinct definition/usage nodes and labeled typed relations | Custom typed element graph; General |
| System breakdown: what composes this scope? | Part definitions/usages, composition, references, multiplicity and occurrence context | Part tree or nested boxes, with repeated usages kept distinct | Native Tree for communication; General/Interconnection basis |
| Internal structure: which ports connect? | Nested features, PortDefinition/Usage, conjugation, connection/interface ends, bindings | Parts with boundary port squares and exact connector docks | Custom port Interconnection |
| Exchanges: what item moves where? | Item types, flow usages, message versus streaming/succession flow, source/target | Flow overlay or summarized transfer graph | Native Dataflow for bounded summaries; custom ports for detail |
| Functions: what is performed and how is it coordinated? | ActionDefinition/Usage, perform usage, parameters, successions, control nodes/structures, send/accept | Action graph with parameters, separate control and item flows, lanes and regions | Custom Action Flow, reusing Workflow styling |
| Modes: what changes state, under which condition? | StateDefinition/Usage, transition usage, entry/do/exit, trigger/guard/effect, parallelism | State graph with nested/parallel regions | Native Lifecycle for flat scope; custom state regions for general coverage |
| Allocation: who realizes which intent? | AllocationDefinition/Usage and source/target intent relationships | Cross-hierarchy links or function/component and logical/physical matrix | Custom allocation matrix and typed links; General/Grid |
| Requirements: what is required under which assumptions? | RequirementDefinition/Usage, subject, assumed/required constraints, nesting, satisfaction, derivation evidence | Requirement graph, hierarchy, subject/constraint compartments and satisfaction matrix | Custom requirement profile; native Architecture only as a bounded summary |
| Verification: what is planned, and what evidence/result exists? | VerificationCaseDefinition/Usage, objective, verify usage, method, procedure, verdict | Requirement/case graph, procedure/action subview and evidence register | Custom composite assurance view; General/Action Flow/Grid |
| Parameters: what is bound, calculated or constrained? | CalculationDefinition/Usage, ConstraintDefinition/Usage, directed parameters, binding, quantities/units | Equation/constraint nodes with parameter docks and equality bindings | Custom parameter network; generic Dataflow arrows are insufficient |
| Analysis/trade studies: how do alternatives perform under assumptions? | AnalysisCaseDefinition/Usage, subject/objective, assumptions, calculations, result | Analysis workflow plus input/result tables and plots | Custom composite analysis view; reuse Workflow and Grid primitives |
| Geometry: what shapes occupy which coordinate frames? | Spatial items, shape, frame, placement, orientation and quantities | 2D/3D arrangement, projection and quantity color maps | Custom spatial renderer; Geometry |
| Configuration: which variants are valid and selected? | Variations/variants, specialization and constraints (§7.6.7) | Variant graph/tree and selection/validity table | Custom variant view; General/Grid |
| Time/history: what ordering or timing is declared/observed? | Occurrences, event occurrences, time slices, snapshots and successions | Sequence for order; time-scaled bands/plots only with supported temporal values | Sequence first; Timeline/Waterfall only with actual dates/durations |

Traceability is cross-cutting: expose exact semantic links in graphs or Grid matrices across requirements, behavior, structure, allocation, analyses and verification. A generic “trace” arrow must not erase whether a link means typing, allocation, satisfaction, verification or ordinary dependency.

Safety/cause-and-effect, security, reliability, maintainability and domain-specific compliance may add further concern-specific views, using appropriate library concepts and/or explicitly modeled extensions. This review does not claim to have completed those domain profiles. They must not be collapsed into an unlabeled generic dependency graph.

## Preserve meaning while improving appearance

The language uses its own definitions/usages and semantic relationships even when symbols look familiar from UML or SysML v1. Preserve type versus usage, owned versus referenced feature, contextual occurrence and multiplicity. Preserve directed transfer versus undirected contact versus equality binding. Preserve control versus item flow, fork/join versus decision/merge, and concurrent versus sequential behavior. Preserve requirement assumptions, subject and satisfaction polarity, and keep verification plans distinct from verdicts and evidence.

The existing ten renderer types provide useful styling, layout and interaction mechanisms. Class/ERD arrows and cardinalities are not automatically equivalent to SysML specialization, feature typing or multiplicity. Timeline/Waterfall layout is not evidence of timing. A default start dot, green success path or status badge is a semantic assertion if readers interpret it that way; it must come from the model or be removed.

Provide an explicit communication-view profile using the clean shared visual language, with exact source inspection available on demand. A future standard-notation mode needs the prescribed v2 graphical distinctions and separate qualification. Do not call the current styled reader a conforming SysML graphical editor.

## Demonstrated coverage and bounds

The [single pump-station design study](examples/pump-station-study/README.md) now supplies **25 presentations covering all nineteen catalogue purposes**. Every presentation is generated from one qualified SysML v2 source revision. The grouped selector includes concerns, context, use cases, membership, definition/usage typing, decomposition, ports, exchanges, actions, parallel state regions, message scenarios, allocations, requirements, verification coverage, parameters/constraints, analyses, alternatives, geometry, configuration and declared timing.

The demonstration adds source-owned semantics to the model rather than inventing diagram content. It contains four declared function allocations, two requirements and their planned verification cases, explicit fork/join and item transfers, two concurrent state regions, a self-message, calculation bindings, two alternative configurations and a dimensioned box envelope. Timing values are declared planning budgets. Verification procedures are plans with no executed verdict.

**Coverage is bounded per profile.** See [the machine-readable family registry](sysml-view-map.json) for the current limits. The browser shows source-owned membership, not imported library expansion. Definitions show direct usage/typing rather than the entire feature specialization language. Action support does not include general loop or performer-lane rendering. Sequence supports local events and acyclic precedence, not arbitrary nested interactions. Geometry supports local rectangular boxes, without invented assembly placement. Analysis evaluates a small explicit scalar/quantity arithmetic profile, not an arbitrary SysML solver. Configuration displays declared variants and selections, without claiming general configuration validity.

These are styled communication views grounded in SysML v2 semantics. Static model qualification, source-to-view fidelity, browser usability, standard graphical-notation conformance and practitioner acceptance remain separate claims. Wider language support and domain-specific concern profiles remain future work.
