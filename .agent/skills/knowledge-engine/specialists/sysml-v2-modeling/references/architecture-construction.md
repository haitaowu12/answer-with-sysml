# From operational concept to connected architecture

Use this branch when a ConOps, stakeholder narrative or existing evidence model
must become a system architecture. Use the existing authoring/change branch for
a narrow edit. This method is informed by Arcadia; the resulting SysML model is
not a Capella repository or a claim of Arcadia conformance.

## Contents

1. [Frame the decision](#frame-the-decision)
2. [Develop the architecture](#develop-the-architecture)
3. [Author and check a native candidate](#author-and-check-a-native-candidate)
4. [Design the review](#design-the-review)
5. [Acceptance and limits](#acceptance-and-limits)

## Frame the decision

Read the actual source, diagrams and tables. State the operational outcome,
system of interest, boundary, lifecycle/configuration and decisions the model
must support. A service can include people, procedures, information and
facilities; choosing that boundary does not select a new IT system or transfer
an external participant's decision authority to the proposed system.

Choose a decision-relevant level of decomposition. Map all agreed source areas
to developed architecture, supporting evidence, an unresolved decision or a
reasoned exclusion. Keep the source inventory available for completeness and
traceability. Do not create a model element for every paragraph just to increase
coverage. Source preservation, interpretation, architecture development and
visual coverage have separate denominators.

Before generation, retain independent review questions with expected facts and
unwanted alternatives: who performs an activity; what crosses a boundary; what
permits admission; who retains responsibility if a handover fails; which
requirement constrains the responsible function; and what evidence could test
it. A compiler's own reconciliation checks do not replace these questions.

## Develop the architecture

| Perspective | Construct | Check by following a real operational thread |
|---|---|---|
| Operational analysis | Outcomes, operational entities/actors, activities, interactions, modes and operational constraints, including work outside the eventual system | Can the participants achieve the outcome? Is each activity's performer visible? Are alternate, failed and recovery situations accounted for? |
| System needs analysis | Selected boundary, system functions, typed inputs/outputs, exchanges with actors and required performance/constraints | Can each allocated system contribution be explained from an operational need? Does every necessary decision consume its inputs and produce a meaningful result? |
| Logical architecture | Candidate responsibility groups, function allocations, interface contracts and allocation rationale | Can an end-to-end function chain cross components without losing the item, condition or responsible party? What coupling or competing allocation does this expose? |
| Physical architecture | Selected implementations, hosting/deployment, physical interfaces, budgets and configuration | Do supplied decisions justify this fidelity? If they do not, leave the physical solution open and retain the logical design. |

Work in increments that connect these perspectives. Complete one thread through
need, functions, exchanges, responsibilities, obligations and planned evidence;
then extend the same shared model across the agreed scope. The first thread is
a technique for establishing the pattern, not permission to stop at a showcase.

### Make the reasoning explicit

- Decompose an activity because its subfunctions have different inputs, outputs,
  responsibilities, conditions or constraints. Reuse shared functions across
  scenarios; preserve each scenario's separate occurrences.
- Give a functional exchange a producing function, consuming function, item,
  direction and applicability. A capability dependency is not a data flow. A
  flow records a potential transfer; temporal precedence, alternatives and
  concurrency require their own behavior semantics.
- Model admission, release and handover conditions. Show the negative branch or
  record its missing decision. Keep permission, notification, acknowledgement
  and acceptance distinct. Do not silently turn an unavailable notification
  into successful receipt, or source silence into a physical failure.
- Keep operational performers separate from candidate logical allocations.
  Explain why functions belong together. Derive logical interface contracts
  from the exchanges that cross the proposed allocation; do not draw arbitrary
  component arrows and infer their content afterward.
- Author requirements about system/service behavior with an identifiable
  subject, condition and observable criterion. Put model-quality questions in
  the review contract. Retain qualitative obligations when formal predicates
  are not justified; a qualitative required constraint is not an executable
  Boolean proof. Keep required bounds separate from achieved values.
- Propose verification methods, configurations, expected observations and
  evidence for each developed obligation. `planned` does not mean executed or
  accepted. Missing targets, demand bases and response bounds stay explicit.
  For a quantitative bound, plan observations on both sides of the boundary and
  at the applicable limit, preserving inclusive/exclusive meaning, units,
  measurement origin and exceptions. A minimum hold measured from confirmed
  delivery needs a pre-minimum case, an at/after-deadline case and an unconfirmed
  delivery case; a general instruction to inspect timestamps is insufficient.
- Label source statements, derivations, design proposals, assumptions and
  accepted decisions. Authorized concept development includes proposing
  alternatives. Do not ask for approval merely to represent a proposal, and do
  not present that proposal as an approved operating process.

## Author and check a native candidate

The bounded architecture authoring profile uses `architecture.json` as a reviewed
recipe. It generates editable SysML source and revision-bound correspondence.
The recipe is not a parser, a native interchange standard or an independent
second model repository. The generated SysML owns the modeled assertions; a
manual source edit invalidates the previous bindings and reader qualification.
Generate a separate candidate and reconcile changes instead of overwriting
manual edits through this partial authoring adapter.

Common records use `id`, `label`, `description`, `basis`, `status` and
`sourceRefs`. Stable IDs must be unique. The recipe contains:

| Collection | Required meaning |
|---|---|
| `scope` | Name, boundary, included/excluded concerns, phase and receiving decision; tailored `requiredConcerns` and `requiredScenarioKinds` |
| `actors`, `operationalActivities` | Operational entities and nested activities, with a referenced `performer` |
| `functions` | Shared system functions, optional parent and `realizes` activity IDs |
| `exchanges` | Source/target function IDs, item, data/control/object kind and condition |
| `logicalComponents`, `allocations` | Nested candidate responsibilities and a primary function-to-component mapping with rationale |
| `contextExchanges` | Directed actor/responsibility boundary contracts with typed payloads; native ports/interfaces retain the external authority boundary |
| `scenarios` | Distinct steps referencing functions; transitions with endpoint IDs and conditions; `entryStep`, `exitSteps`, `exitGuards` and explicit fork/join groups where concurrent contributions are required |
| `stateMachines` | Subject, states, initial state, event/guard/effect transitions and terminal or ongoing lifecycle disposition |
| `requirements` | Subject, statement, condition, criterion, rationale, parent/source IDs and planned verification IDs; optional bounded numeric/duration constraint |
| `verificationCases` | Requirement IDs, method, setup, expected result and `planned` status |
| `decisions`, `insights`, `coverage` | Alternatives and affected records; supported consequences; source/journey dispositions |

The reader also retains `parameters`, insights and evidence records as authored
analysis. Do not call an analytical item native-resolved unless a checked binding
establishes its native counterpart. Formal numeric/duration requirement bounds
are separately checked native constraints; they do not assign achieved values.

Author requirement fields and choose diagram content using [requirements and viewpoints](requirements-and-viewpoints.md). The compiler uses the requirement ID as its short name, the label as its declared name, and the statement as its documentation. Older recipes retain their condition and criterion as the fallback statement.

Name each scenario action for what the participant does, and write each branch
condition and completion criterion as a short phrase that makes sense on an
arrow. The compiler uses these phrases for the native action and Boolean
predicate names. It retains the recipe IDs in the bindings, uses the referenced
function label when a step label is absent, and adds an ID to disambiguate
repeated names within a scenario. Review predicates remain Boolean attributes
with unspecified values.

The generated model declares an action-flow view within each scenario and
review scopes for operational context, function decomposition, logical
interfaces, lifecycles, and requirements with planned verification. The
coordinated HTML reader and SVGs are generated with populated layouts from the
same revision. Native view declarations specify type and scope. For a directly openable
SysON diagram, use the saved review view workflow below.

For a required concurrent contribution, define a scenario `parallelGroups`
entry with `id`, `from`, `branches` and `join` step IDs. Mark outgoing branch
transitions `kind: parallel` and incoming completion transitions `kind: join`.
The compiler inserts actual ForkNode/JoinNode occurrences. A join requires all
its declared contributions: an optional branch needs an explicit bypass/outcome
or a separately scoped scenario whose entry conditions require that branch.
Never represent an optional skipped contribution as a completed one. Guards
remain unevaluated review predicates; no deadlock-free execution is claimed.

An optional `formalConstraint` on a requirement has `attribute`, `quantity`
(`duration` or `number`), `operator`, `value` and, for duration, `unit`
(`s`, `min`, `h` or `d`). The subject receives the corresponding attribute and
the requirement receives a required comparison. Independent native checks
verify the actual subject path, operator, bound and resolved unit. Keep clock
origins, applicability, exceptions and measurement conditions in the requirement
and planned case even when only the bound is formally expressed.

From the installed native skill directory:

```text
python3 scripts/sysml.py architecture --architecture /project/architecture.json --output /project/candidate --qualify
```

The command builds the candidate, runs the installed pinned engine, reconciles
native correspondence, assesses authored graph adequacy, and generates the
coordinated reader. Use a new output directory. `--evidence` can retain a prior
source catalogue once in the reader. Without `--qualify`, outputs remain an
authored draft with language/native correspondence unverified. `doctor` and
the existing runtime guide own setup; no network runtime is implicit.

Use `architecture_model.py`, `architecture_check.py` and
`architecture_review.py` directly when a project needs separate steps; consult
their `--help`. The native checker reads a fresh sealed report, matching model
bytes and recipe correspondence. Generated translation expectations establish
translation consistency. Independent source questions and populated-view
inspection establish different evidence.

The fictional `workbench/fixtures/architecture/tool-library` exercise supplies
a full small recipe and an independent source brief. Keep project-specific
sources and generated studies outside the installed skill. The authoring
profile currently uses one primary logical allocation per function; represent
alternative allocations as separate configurations, not silently overwritten
rows. A verification definition spanning different requirement subjects needs
an explicitly authored common subject outside this bounded recipe profile.

## Design the review

Provide one entry point and one evidence inventory. Select each architecture
view by a reader's question, perspective, scope and exact revision. Typical
questions are operational responsibility, functional decomposition, exchange
content, logical allocation, scenario conditions, state change, requirements
and verification, and unresolved architecture decisions.

Use meaningful activity names on diagrams. Preserve occurrence IDs and native
targets in the inspector. Show a selected thread and its boundary exchanges;
avoid a whole-model trace web as the opening view. Put full source passages,
definitions and evidence on demand. Keep source-to-model navigation intact.
Missing architecture relationships should produce an explicit gap, not a
replacement catalogue with a new title.

Global declaration/requirement inventories appear once. The native `catalogue`
helper consolidates only semantically identical global inventories and retains
navigation aliases. Shared elements in different questions or relationships are
legitimate views and remain distinct. Do not deduplicate by element counts.

## Acceptance and limits

Review the actual candidate against these separate evidence classes:

1. **Source interpretation:** inspect the passages, roles, conditions, conflicts
   and proposed additions. Coverage is not entailment.
2. **Authored architecture:** check typed endpoints, decomposition, allocation,
   connected function paths, reachable scenarios, completion/recovery
   dispositions, requirement criteria and planned checks. Resolve errors and
   retain open engineering decisions as review findings.
3. **Native translation:** parse/resolve the exact source; independently
   reconcile performance, flow parameters, allocation endpoints, subjects,
   verification targets and guarded/state relationships. Reject stale bytes,
   swapped endpoints and documentation-only substitutes.
4. **Reader behavior:** inspect populated scoped views; exercise selection,
   source access, perspective changes, conditions, narrow layouts and exports.
   Confirm that a source/recipe change reaches the regenerated output and a
   stale recipe/report cannot claim qualification.
5. **Engineering insight:** explain a consequence supported by the model, the
   decision it affects and the evidence that could resolve it. Report coupling,
   missing authority, unacknowledged handovers or missing performance inputs
   only when the modeled facts support that conclusion. Do not invent scores,
   reliability, capacity, readiness or simulation results.

This profile does not execute opaque guard predicates, prove guard exclusivity,
simulate queues or physical behavior, certify safety, transfer decision rights,
or accept a system. Planned verification remains planned. An open design
decision can coexist with a useful, consistent concept model; it must not be
hidden by a single green completeness label.

## Primary method references

- [Arcadia questions and answers](https://mbse-capella.org/arcadia-qna):
  operational scenarios, functional exchanges and architecture distinctions.
- [Arcadia User Guide](https://mbse-capella.org/resources/arcadia-reference/Arcadia%20User%20Guide.pdf):
  operational, system, logical and physical engineering perspectives.
- [NASA logical decomposition](https://www.nasa.gov/reference/4-3-logical-decomposition/):
  functions, inputs/outputs, interfaces and end-to-end behavior.
- [NASA technical requirements definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/):
  requirement rationale, traceability and verifiable obligations.
- [OMG SysML 2.0 language](https://www.omg.org/spec/SysML/2.0/Language/PDF):
  native language semantics; the configured engine's qualification remains
  separate from full language or vendor conformance.


## Saved review views in SysON

Generate the architecture candidate with the normal `architecture --qualify`
command. Then publish the selected action flow to an authorized SysON
2026.11.0 instance using its GraphQL API. This creates a new review project
from the candidate's `model.sysml`, populates the named representation,
saves the geometry, and returns a direct link.

```sh
python3 scripts/sysml.py syson-review --candidate /project/candidate \
  --scenario SC03R --layout /project/handover-layout.json \
  --url http://127.0.0.1:18080 --project-name "Assistance handover review"
```

Author the layout alongside the project recipe when selecting the scenario
for review. Use stable step IDs for the centers of the action boxes and
`start` and `done` for the entry and completion markers. Choose a descriptive
`name`, or let the command use the scenario label and ID. Coordinates are
diagram pixels. This three-action example keeps the acceptance path and the
return loop apart. The keys must match the actual recipe.

```json
{
  "name": "Assistance handover recovery",
  "positions": {
    "start": [24, 110],
    "Identify": [170, 110],
    "Retain": [170, 335],
    "Accept": [500, 335],
    "done": [500, 555]
  },
  "conditionOffsets": {
    "T02": [-75, 5],
    "exit:Accept": [-160, -10]
  }
}
```

Allow room between boxes for the longest condition. Use short, faithful
arrow labels and keep full criteria in the scenario documentation. Optional
`conditionOffsets` move labels relative to the edge center. Use the
transition ID or `exit:<step-id>` as the key. Include the branch that
retains responsibility and the branch that completes the handover.

The adapter checks model and recipe bytes against their bindings, verifies
the created diagram's actions, endpoints and condition texts, and reads
back the saved label and geometry. Open the returned link in a fresh tab
and then reload it. Confirm that the complete flow and its long labels
are readable at the intended canvas size without adding or arranging
elements. Adjust the layout input and regenerate if branches compete for
space. Keep the layout JSON with the recipe so another build can reproduce
it. This adapter covers a selected scenario without explicit fork/join
groups. Other SysON representations and other tools need their own
graphics adapter. The portable model and offline reader can still be
delivered through the normal architecture workflow.
