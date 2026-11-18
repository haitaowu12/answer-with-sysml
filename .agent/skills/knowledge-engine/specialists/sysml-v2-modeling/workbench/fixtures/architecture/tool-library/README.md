# Community tool library architecture fixture

This fictional ConOps exercises the ConOps-to-architecture method in a domain
different from the airport redevelopment example. It describes no real
organisation, policy, approved system or safety standard.

The authored input covers all eight source clauses through operational actors
and activities, shared functions and typed exchanges, proposed logical
allocations, actor/service interface contracts, three scenario families,
identified-tool state, source requirements and planned verification. Unknown
decision freshness, registry waiting time, opening hours, additional hold
duration, demand, tool counts, volunteer capacity, turnaround and notification
performance remain unvalued. Physical implementations are outside the scope.

## Inputs and independence

- `source.md` is the original fictional brief with clause locators TL-01–TL-08.
- `architecture.initial.json` preserves the recipe frozen before generation
  and the separately prepared acceptance questions were read.
- `architecture.json` is the maintained recipe after the recorded review fix.
  It is a bounded authoring input, not a native SysML interchange format or a
  second model repository.
- `review-questions.json` records author-side source questions and unwanted
  alternatives before generation.
- `evidence.json` retains the eight source clauses once for the reader's
  evidence tab; it is a direct source inventory, not architecture coverage.
- `intake-freeze.json` binds those inputs before native generation and before
  the separately withheld acceptance exercise was read.
- `acceptance-questions.json` retains the ten separately prepared source
  questions (the original brief filename in that record refers to the exact
  source bytes retained as `source.md`).
- `acceptance-review.initial.json` records nine supported questions and one
  partial result on the frozen candidate. The hold verification setup did not
  explicitly include observations before the two-hour minimum and at/after
  the chosen deadline.

The recipe deliberately retains the scenario step ID `accept`. The first
normal-entry-point native run found that the adapter did not escape this SysML
keyword. The fix belongs to generic native-name handling; renaming the source
step would mask the defect. This input became a regression for that fix. It
therefore does not establish a wholly unseen, first-attempt end-to-end success.

The maintained recipe changes only the planned hold-verification setup and
expected observations. It adds the missing boundary observations, the actual
confirmed-delivery origin, no-confirmation behavior, withdrawal/new-fault
exceptions and reasoned extension. The original recipe and review are retained;
this repair is reassessment of a known case, not a second blind trial.

`acceptance-review.final.json` records ten supported source questions after
that repair. `qualification-summary.json` records the observed normal-CLI
results: authored and native checks passed, the reader was generated with all
eight source clauses, and fifteen engineering decisions/parameters remained
open. Reader generation is separate from a completed interaction trial. No
verification case or service-performance test was executed.

## Reproduce through the normal entry point

Run from the native skill directory with its verified local runtime installed:

```sh
python3 scripts/sysml.py architecture \
  --architecture workbench/fixtures/architecture/tool-library/architecture.json \
  --evidence workbench/fixtures/architecture/tool-library/evidence.json \
  --output /tmp/tool-library-review \
  --package ToolLibraryArchitecture \
  --qualify
```

Use a new output directory and keep generated model, reader and qualification
evidence outside the installed source package. The workflow retains exact model
bytes, bindings, authored adequacy findings and native reconciliation. Source
interpretation and populated reader review remain distinct acceptance work.

## Review the causal distinctions

Follow the two concurrent preparation contributions into the readiness gate:
the registry owns eligibility while the steward owns condition. Inspect the
negative alternatives and the selected member/tool identities. Then follow
notice delivery confirmation into the minimum two-hour hold. Queueing and an
absent acknowledgement must not acquire a fictional delivery timestamp.

Collection requires member/tool matching and accepted terms/receipt before
custody transfer and on-loan state. Return requires actual steward receipt;
repair completion requires reassessment and accountable release before
availability. Notification, permission, custody and accepted condition are
different facts.

The formal duration criterion retains a required bound, not an achieved service
measurement. Guard text remains an unevaluated review predicate. Verification
is planned throughout. The fixture demonstrates a bounded, reproducible set of
constructs and defect checks; it does not prove arbitrary-domain adequacy,
behavior execution, throughput, practitioner usability or system acceptance.
