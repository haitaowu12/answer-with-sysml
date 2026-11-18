# Model-backed explanation design

Read this before authoring an audience-facing answer. The engineering reader is an
inspection tool, not automatically a successful explanation. A valid model and a
large diagram count do not prove useful scope, visual quality or interaction.

## Decide the story before the template

Write a short private answer plan: audience, question, take-away, what must be
understood, and the sources that can establish it. For each important reader
question identify the model concepts/relations that answer it, the visual form,
and any justified omission. Do not reduce a broad “how does it work?” request to
three easy views merely because the renderer already supports them.

Use information shape, not a favourite diagram: nested parts for composition;
sequence or swimlane for responsibility over time; contrasting cases for a
boundary/choice; a dependency graph for impact; a matrix for coverage; a state
machine for lifecycle; an annotated concrete example to connect abstractions.
Several complementary representations should expose the same model, not invent
independent claims. Expand the model where a question exposes missing semantics.
For a selected process path, retain every transition guard and provide the full
behavior for branches and loops. Adjacency alone does not preserve conditional
meaning; never turn a guarded success path into unconditional arrows.
A comparison or editorial view is a model-backed explanatory projection, not
necessarily standard SysML notation. Keep that distinction in its evidence.

Do not turn teaching rules into system requirements to inflate the model. Model
actual participants, artifacts, responsibilities, relationships, inputs/outputs,
conditions and relevant failure/recovery paths. Add requirements when the source
states a constraint or a clearly labelled design requirement is genuinely useful.

## Source roles

Start with supplied documents. Research missing technical facts in authoritative
primary sources. State in the source drawer what each source establishes: an open
format specification, a host implementation, a product limit, or an example.
A format specification does not establish every host's behavior. Distinguish
source facts from engineering interpretations and concrete illustrative choices.
Use citations where they support claims, not as an unexplained decorative footer.
For private or deployment-specific explanations prefer the actual configuration
and distinguish it from generic guidance; do not expose private sources in a
public package.

## Visual direction

Choose a topic-appropriate visual direction explicitly. There is no mandatory
green/teal palette. Use restrained semantic accents, meaningful scale, whitespace,
and a clear reading order. Do not recolor identical cards and call it variety.
Choose paper/editorial for careful reading, blueprint for structural inspection,
or a contrast-rich product style for interaction when they fit the audience.
Colour alone must not encode meaning. Avoid stock subtitles, process notes and
boilerplate caveats; retain concise qualifications where omission would mislead.

The Answer Me With HTML donor's useful pattern is question-led navigation plus
purpose-built representations, not literal copying of its theme or visual code.
Keep donor provenance in DONORS.md, outside the audience narrative.

## Delivery surface is part of correctness

Use real links for section navigation. All core content must remain accessible
with scripting disabled; only enhance after successful initialization. Do not
hide unvisited answers at source-generation time. Never ship buttons whose only
function depends on JavaScript in a script-blocking attachment preview. Offer a
readable static document there and test the interactive file in a browser.

For a new recipe-backed answer, `scripts/render_explanation.py` provides a
progressively enhanced answer shell: identity-bound model cards, links, native
SVGs and evidence details. It validates exact recipe/model/binding hashes and
supports composition, process and contrast layouts. It is a starting point, not
a substitute for subject-specific visual design. For direct native authoring,
use the qualified reader's identities and equivalent source-grounding checks;
do not invent a second recipe just to use this adapter.

## Acceptance

Test the exact final artifact, not an earlier reader or build directory:
- Each navigation link changes the visible destination; deep links and Back work.
- With JavaScript disabled, every answer and source/model download remains usable.
- Keyboard activation, focus visibility, repeated switching and narrow-width
  layout work. Every custom control has a defined, tested observable effect.
- Inspect desktop and mobile screenshots for clipping, unreadable labels, density,
  empty space and duplicated visual forms. A syntax pass is not visual acceptance.
- Verify answer claims and depicted relations against source and model. Native
  diagrams remain native projections; additional visuals carry model IDs and do
  not imply simulation or measured outcomes.

Keep the execution receipt separate from the answer. Record exact artifact hashes,
viewport sizes, observed interactions, screenshot paths and any blocked checks.
If browser execution is blocked, say so in the delivery status; do not mark it
passed or bypass a sandbox denial. Deliver a no-script-capable artifact meanwhile.
