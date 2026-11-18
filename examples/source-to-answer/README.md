# From a source document to a model-backed answer

**Question:** What must happen before a tool can be offered for loan, who owns
those decisions, and does a completed repair report make the tool available?

The [fictional source brief](../../.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/architecture/tool-library/source.md)
contains eight numbered clauses. The agent-guided interpretation is retained in
the [authored architecture recipe](../../.agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/architecture/tool-library/architecture.json),
with a separate source-clause inventory and open decisions. The native model is
generated from that explicit interpretation, not inferred from a finished drawing.

## Reproduce

After installing the pinned runtime, run from the repository root:

```sh
python3 .agent/skills/knowledge-engine/specialists/sysml-v2-modeling/scripts/sysml.py architecture \
  --architecture .agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/architecture/tool-library/architecture.json \
  --evidence .agent/skills/knowledge-engine/specialists/sysml-v2-modeling/workbench/fixtures/architecture/tool-library/evidence.json \
  --output output/tool-library --package ToolLibraryArchitecture --qualify
```

[Open the generated HTML answer](answer.html) · [Native SysML model](model.sysml) · [Claim provenance](provenance.json)

Download/clone the repository and open `answer.html` from this example folder. Keep its `diagrams/` and linked model/check files together; this architecture-study reader is a portable folder, unlike the self-contained Archify reader.

Use a fresh output folder. The output preserves the model, identity bindings,
qualification evidence and HTML reader. Open `output/tool-library/review.html` to explore
purpose, boundaries, functions, interfaces, scenarios, states and evidence.

## Answer grounded in the source

| Question | Answer | Source |
| --- | --- | --- |
| Can preparation happen in parallel? | Yes. Registry eligibility and steward condition inspection are independent contributions; both must support readiness for the selected member and identified tool. | TL-04 |
| Who decides eligibility? | The external registry, not the tool service or steward. | TL-02, TL-04 |
| Does a repair report release quarantine? | No. The steward must reassess the tool as fit; the coordinator can then release it. Remaining defects retain quarantine. | TL-07 |
| When does the minimum hold begin? | At confirmed delivery of the ready notice, not when it is queued. No confirmation means pending notification, not an invented start time. | TL-05 |

The reader and native model make these distinctions inspectable across actor,
functional, interface and behavior views. The source remains the authority for
what was requested; proposed architecture decisions remain identifiable as choices.

This is a reproduced maintained fixture, not a new blind test of arbitrary
source interpretation. Verification cases are plans, not executed service tests.
