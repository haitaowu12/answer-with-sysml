# Donor ledger

| Component | Source | Adopted role | Version record |
| --- | --- | --- | --- |
| Answer Me With HTML | https://github.com/QingYunA/answer-me-with-html | Method-level learning: question-led panels, representation by information shape, explicit visual direction, content/interaction acceptance. No donor code copied. | Reviewed 2026-11-18, commit 912bad4cb7ccdb3729262bf885f5280b3da941ee |
| Archify | https://github.com/tt-a1i/archify | Native layout, self-contained HTML readers and diagram schemas | `resources/tools/archify/SOURCE.json` |
| SysML v2 Pilot Implementation | https://github.com/Systems-Modeling/SysML-v2-Pilot-Implementation | Separately installed parser, semantic model and standard library | Native `workbench/config/reference-pilot-lock.json`; release 2025-09 / kernel 0.52.0 |
| OpenSysML | See native `references/view-workspace-architecture.md` | Retained optional view-workspace source | Native `diagram-ui` license and notices |

The model qualification and presentation adapters are maintained together here.
Upstream changes are reviewed before adoption; this repository does not install
or update donors automatically. Compare pinned source records, preserve notices,
run regression tests and inspect the resulting reader before changing a pin.
