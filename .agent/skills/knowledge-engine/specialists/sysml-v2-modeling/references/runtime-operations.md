# Modeling runtime operations

## Start here — one package

All required instructions, executable tools, examples and checks live in this skill folder. Resolve it from this `SKILL.md`; no project notebook, audit worktree or Downloads path is required. Run commands from this folder, or use the absolute path to `scripts/sysml.py` from any working directory. User input/output paths are caller-relative.

```sh
python3 scripts/sysml.py doctor
python3 scripts/sysml.py demo --port 5224
```

`doctor` checks package integrity, Python 3.10+, Java 21+, Graphviz and the pinned engine/library. The local engine lives in `.runtime/`. If it is absent, install the official Pilot `2025-09` archive with `python3 scripts/sysml.py setup --archive /path/to/jupyter-sysml-kernel-0.52.0.zip`. The source URL and exact hashes are in [the runtime lock](../workbench/config/reference-pilot-lock.json). Setup verifies the runtime and preserves its license files; it does not install a Jupyter kernel or modify machine configuration. Never substitute a regex parser for authoritative validation. See [package scope](../PACKAGE.md) for transfer and system dependencies.

`demo` opens a loopback-only workbench over the included fictional pump example. Browser drafts never write canonical source. Engineering/Stakeholder modes and objective-led review routes use one validated report. Use the user's preferred browser and inspect the actual interaction, not just generated markup.

The Lab's Project route records a brief and open decisions, downloads/reopens an explicit local project file (source, baseline, notes, view recipes and change history), and exports a frozen reader review or model source. Develop model supports bounded integer-minimum, component, ordered-scenario and performance-assignment proposals with fresh engine validation and exact-base apply. These are local project changes, not authenticated shared approval or full graphical authoring. Custom views appear in the main selector and share diagram, register, matrix, trace and responsibility presentations across audiences. Preserve downloaded project files; browser storage alone is not a project backup.

## Execute without path hunting

```sh
python3 scripts/sysml.py qualify --source /model/model.sysml --views /model/views.json --output /evidence/new-validation
python3 scripts/sysml.py context --report /evidence/new-validation/report.json --source /model/model.sysml --target 'System::subsystem' --output /evidence/context.json
python3 scripts/sysml.py propose --report /evidence/new-validation/report.json --source /model/model.sysml --proposal /intake/proposal.json --output /evidence/new-candidate
python3 scripts/sysml.py serve --source /model/model.sysml --views /model/views.json --reviews /model/reviews.json --port 5224
```

The runtime arguments are resolved internally. `context` requires a verified local report receipt, accepts the same occurrence keys as the human scope picker, and bounds each serialized response to 16 KiB by default with explicit omissions and continuation. It refuses a stale source/report pair. `propose` writes separate baseline/candidate/diff/receipt files; it does not validate, approve or promote the candidate. Re-qualify, inspect semantic changes and run independent expected-fact/evidence checks before representing it as accepted. Existing user authorization governs routine faithful edits; ask at a material unresolved engineering decision, not after every reversible step.

Additional commands: `evolution`, `check`, `evidence`, `assess`, `capacity`, `test`, `regressions`, `community`, `acceptance`. Use `<command> --help` for exact arguments. `test` runs the included Python regression suite. UI development checks are optional in `workbench` using its locked npm development dependencies; the running UI needs no Node service.

## Evolve a controlled local baseline

Use `evolution impact --manifest /change/source-change.json --output /change/transaction` for a revised external artifact. Supply exact old/new source anchors and recorded dependency links. The result distinguishes direct, possible and unknown impact, retains removed links, and separates historical observations from new applicability annotations. Inspect the candidate and independent checks, then use `evolution promote` with an exact-bound recorded disposition. Promotion requires fresh managed qualification and the expected unchanged baseline; it keeps the prior source and receipt. This is a single-file local workflow on macOS/Linux with cooperating-writer locking, not authenticated shared approval.

Use `evolution plan` to expose missing setup, independent oracle, instrumentation/calibration applicability, configuration, evidence and authorization. Every plan remains non-executable until the responsible project process releases it. See [the full schema and examples](../workbench/tools/reference-pilot/LIFECYCLE.md).

Reports bind frozen source and view inputs, producer snapshots and all rendered artifacts. Preserve the entire qualification directory when transferring evidence. The digest chain detects changed or mixed local evidence; it is not an authenticated signature. A matching view-review basis also requires the complete recipe, including concern, target, renderer and styles. It does not establish that a person completed the review.
