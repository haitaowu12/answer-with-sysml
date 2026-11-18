# How agent skills work

[Read the explanation](answer.html) · [Explore the model](model.sysml) · [Source evidence](source.md)

Seven reader questions connect package anatomy, progressive disclosure, execution
boundaries, a source-to-SysML task, improvement and portability. The HTML is a
standalone, no-script-capable document with model downloads. Evidence drawers
identify the native elements behind its explanatory cards; the attached native
flow is a visual projection, not an interactive model editor.

The Agent Skills specification describes the open format. OpenAI documentation
supports Codex-specific statements. Neither is a substitute for a particular
host's actual configuration. Lifecycle quality gates are marked as a proposed
teaching design, not presented as hidden product implementation.

## Reproduce

From the repository root, with the pinned native runtime already set up:

```sh
python3 .agent/skills/knowledge-engine/specialists/sysml-v2-modeling/scripts/sysml.py architecture \
  --architecture examples/agent-skills/architecture.json --output output/agent-skills --qualify
python3 examples/agent-skills/check_meaning.py --bundle output/agent-skills
python3 scripts/render_explanation.py --plan examples/agent-skills/plan.json \
  --bundle output/agent-skills --source examples/agent-skills/source.md --output output/agent-skills-answer.html
python3 scripts/check_explanation.py output/agent-skills-answer.html
```

The checked-in plan binds the exact model bytes. If a runtime/model change alters
them, review the regenerated semantics and update `modelSha256` in a copied plan;
do not weaken that check. Source locators, model IDs, relationship meaning and
question coverage require review alongside native qualification.

For palette selection when exporting native diagrams independently, the native
`architecture-review` command accepts `--theme paper`, `blueprint` or `ink`.
The answer plan uses the same explicit theme names. Themes change presentation,
not model labels, identities or relationships.

Static delivery checks do not certify browser behavior or visual quality. Test
the exact delivered HTML in the intended browser, at desktop and narrow widths.
