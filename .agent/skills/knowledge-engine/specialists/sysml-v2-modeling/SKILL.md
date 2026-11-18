---
name: sysml-v2-modeling
description: Use when creating, querying, reviewing or evolving source-grounded SysML v2 models and stakeholder views from documents, interfaces, requirements or dialogue. Owns the bounded local modeling workbench; generic engineering analysis does not require its runtime.
---

# SysML v2 collaborative modeling

Maintain the user's system understanding as source-grounded model assertions. Supporting documents, unresolved decisions and observations retain their own authority. Human views and agent contexts are projections of the same model revision.

## Start from the engineering question

Establish the audience, decision/review question, source basis, system boundary and required facts in the existing project brief or view recipe. Identify whether the work is concept development, change, assurance, operations or retirement. Reuse the project method and records; ask only for a missing engineering decision that materially changes the result.

Select the relevant branch and read its instructions before execution:

| Task | Read | Expected output |
|---|---|---|
| Build or evolve system understanding | [Collaborative method](references/collaborative-method.md) | Distinct operational activities, system functions, logical responsibilities and physical realization as relevant |
| Transform a ConOps or evidence catalogue into architecture | [Architecture construction](references/architecture-construction.md) | Connected operational activities, typed functional exchanges, logical allocations, scenarios, requirement subjects and planned checks in one review workspace |
| Author from documents, tables or dialogue | [Element authoring procedures](references/element-authoring.md), [Authoring and verification](references/authoring.md), [model package](workbench/tools/reference-pilot/MODEL_PACKAGE.md), [checked syntax](references/validated-syntax.md) | Source-linked model, explicit unknowns and independently expected facts |
| Query or propose a model change | [Agent workflow](workbench/tools/reference-pilot/AGENT_WORKFLOW.md) | Bounded current context or separate candidate/diff; no implied acceptance |
| Qualify, serve, transfer or promote a local baseline | [Runtime operations](references/runtime-operations.md) | Managed qualification/evidence or exact-base local transaction |
| Deliver/review views or repair generation | [MBSE view catalogue](references/view-catalogue.md), [Delivery acceptance](references/delivery-acceptance.md), [requirements and viewpoints](references/requirements-and-viewpoints.md) | Populated, inspected views with declared scope and remaining limitations |
| Plan verification, commissioning or source-change impact | [Lifecycle contract](workbench/tools/reference-pilot/LIFECYCLE.md) | Distinct planned checks, executed results, applicability and acceptance states |

The reasoning method is Arcadia-inspired; it does not claim Arcadia/UAF conformance. Use the smallest analysis and concern-specific views that answer the question.

## Check runtime availability

Resolve all package paths from this `SKILL.md`. Run from this directory, or invoke its `scripts/sysml.py` by absolute path; user input/output paths remain caller-relative.

```sh
python3 scripts/sysml.py doctor
```

`doctor` checks the source package, Python, Java, Graphviz and pinned engine/library. Read [runtime operations](references/runtime-operations.md) for setup, demo, command details and transfer. If a dependency is absent, report the exact blocked operation and continue source/engineering analysis where possible. Do not substitute a regex parser for authoritative language validation or claim validation that did not run.

Keep model, candidate and generated evidence in the user project/evidence workspace. Do not write them into the installed skill or treat browser storage as a backup.

## Execute and verify

1. Inspect source evidence and the current baseline. Preserve conflicting sources, unknown values and material decisions before modeling; new documentation does not automatically authorize a design remedy.
2. Author or propose the smallest relevant change. For architecture work, develop operational outcomes, system functions, exchanges and responsibility allocations before expanding the source catalogue. Complete the agreed scope through connected increments. Keep model ownership, occurrence identity, typing, direction, multiplicity, units, conditions and evidence status. A connection is not automatically a flow; a design assertion is not proof.
3. Qualify with the pinned SysML 2.0/KerML 1.0 engine and inspect resolved facts. Run independent expected-fact and evidence checks; parsing alone does not establish source fidelity.
4. Generate views and bounded agent context from the same qualified revision. For architecture recipes, give scenario actions and branch conditions reader-facing names and use the generated native view scopes and coordinated reader. When delivering a scenario in SysON, use the [saved review view workflow](references/architecture-construction.md#saved-review-views-in-syson) to generate a named, populated diagram with its layout and direct link. Give each view a distinct question; keep full evidence inventories once behind contextual source access. Reject stale source/report pairs and expose omissions. Re-qualify a proposed candidate before representing it as validated or accepted.
5. Inspect the populated deliverable against [delivery acceptance](references/delivery-acceptance.md): readable labels, identifiable endpoints, conditions, scope and source access. A screenshot or artifact count alone is insufficient.
6. Return model source, useful views, source/evidence/decision records and the actual checks performed. Identify the next unresolved engineering question and untested scope.

For a supported-scope generation defect, diagnose its owning layer and repair/regenerate within the authorized scope; do not patch emitted SVG/HTML or distort valid source to accommodate a renderer. Test the failing input and affected independent cases before claiming generalization. A changed skill or generator is not an incidental requirement for ordinary model authoring.

## Completion boundaries

The package supports bounded local modeling, declared-behavior explanations and single-file baseline evolution. It does not establish full-language notation, simulation, persistent native graphical authoring, authenticated shared approval or commissioning readiness. The contributor pilot and standalone workbench do not qualify a separate product's semantic runtime.

Keep structural validation, semantic checks, visual findings and human acceptance distinct. For unsupported scope, state the missing capability and a supported alternative where available. Preserve entire qualification directories when transferring evidence; their digest chain detects mixed or changed files but is not an authenticated signature.
