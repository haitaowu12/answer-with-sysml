---
name: answer-with-sysml
description: Explain system concepts, architecture, interfaces, requirements and behavior with native SysML v2 models and interactive HTML views. Use for model-backed MBSE explanations, stakeholder reviews and reusable system studies, keeping an editable model behind the visuals.
---

# Answer with SysML

Use this repository as the skill directory. Keep its supporting folders together.

## Workflow

1. Read the supplied source documents and the user’s question. Preserve source revision and locators (clause, page, paragraph or line range). Interpret the system before drawing it: boundary, stakeholders, responsibilities, functions, interfaces, behavior, constraints and unresolved decisions. Separate source facts, engineering inferences and proposed choices.
2. Build a source-to-model mapping. For each answer claim, retain its source locator and the model element or relationship representing it. Ambiguities stay unresolved; never fill a gap with an invented fact. Before authoring, freeze source-derived review questions and negative/unknown cases using `references/source-interpretation-review.md`.
3. Read `.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/SKILL.md` for native modeling. For a new study, read its `references/architecture-construction.md`; for existing models, read `references/view-catalogue.md` and `references/element-authoring.md` as needed.
4. Author or update the native `.sysml` source and explicit view recipes. Preserve recipe IDs for unchanged concepts; inspect native bindings and qualified-name changes rather than assuming persistent cross-run UUIDs. Keep operational, functional, logical and physical descriptions distinct.
5. Run the native package's `doctor`; install only its pinned official runtime using `setup --archive` when authorized. Run `qualify` against the exact source and recipes. Never substitute a handwritten success report.
6. Read `resources/tools/archify/SYSML.md`, then build selected views with `python3 scripts/archify.py sysml-reader`. Use a new output directory and a matching managed qualification report. The model owns meaning; layout does not establish semantics.
7. Inspect the actual HTML at desktop and narrow widths. Check readable labels, cross-view selection, source inspection, directional relations and matrices. Run `python3 -B -m unittest discover -s tests -v` after modifying the reader.
8. Before delivery, perform a separate source-first interpretation review against the qualified model and regenerated views. Check branch outcomes and joins, message versus completion phases, every boundary exchange, and revision identity/answer changes. Inspect destination functions and terminal dispositions, not just arrow labels. For recipe-based authoring, record explicit expectations and run `python3 scripts/review_source_interpretation.py --source SOURCE.md --recipe architecture.json --review source-review.json`; its pass checks receipt consistency, not source entailment. For direct native-model work, perform the equivalent source/model/view review and retain its evidence without inventing an architecture recipe or second model. Correct discrepancies or leave the affected claim unresolved.
9. Answer the user’s actual question with selected views and concise subject-focused explanation. Use the source-to-model mapping to inspect support for each claim; qualification of syntax/facts alone does not prove that the interpretation is faithful. Keep alternate representations tied to the same native model.
10. Deliver the reader, native model and recipes together. After changes, requalify and regenerate. Preserve the last good output if qualification fails.

## Output contract

- Let visual hierarchy and layout explain the subject. Keep internal process notes, unnecessary subtitles and defensive commentary out of rendered outputs.
- Retain labels, units, source attribution and qualifications needed to understand scope accurately.
- Never present declared verification as executed testing, a view as simulation, or a rendered model as full standards certification.
- Keep private source and reports local. Before sharing, inspect the embedded source and sidecars as well as the visible page.
- Never silently repair unknown semantics or flatten unsupported concurrency into a sequential story.

For a worked source-document → authored model → grounded HTML answer, read `examples/source-to-answer/README.md`. For follow-up questions reuse the existing model; for source changes compare revisions, update affected elements and evidence, requalify, then regenerate.

See `README.md` for installation and a reproducible example. Licensing and donor history are separate in `NOTICE` and `DONORS.md`.
