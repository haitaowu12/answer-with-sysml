# Agent skills: format, runtime and improvement
Reviewed 18 November 2026. Paraphrased evidence and explicitly bounded teaching design.

## S1 · Open format, not a vendor runtime
Agent Skills overview, “What are Agent Skills?” and “Open development”: https://agentskills.io/home
Agent Skills is an open package format originally developed by Anthropic. It packages reusable procedural knowledge for compatible agents. It does not specify one universal agent implementation. Reuse of a folder does not establish identical behavior on different hosts.

## S2 · The package contract
Agent Skills specification, “Directory structure”, “SKILL.md format”, “Optional directories”: https://agentskills.io/specification
SKILL.md is required and has YAML metadata followed by Markdown instructions. Name and description are required. Scripts, references and assets are optional; they provide executable helpers, detailed reading and reusable output resources respectively. Compatibility metadata can record environment requirements.

## S3 · Progressive disclosure
Agent Skills specification, “Progressive disclosure”: https://agentskills.io/specification
The catalogue exposes metadata first. The complete chosen instructions enter context on activation. Supporting resources are accessed when relevant, not all at startup. References and templates are not themselves tool invocations.

## S4 · Host discovery and trust
Agent Skills client implementation, “Discover skills”, “Trust considerations”, “Cloud-hosted and sandboxed agents”: https://agentskills.io/client-implementation/adding-skills-support
A host determines where packages are available, how names are resolved, and which repositories are trusted. A remote host may need packages provisioned rather than assuming access to a user's local folders. The guide recommends checking trust before loading project instructions.

## S5 · Codex invocation and distribution
OpenAI, Build skills, “How ChatGPT and Codex use skills”, “Where Codex loads local skills”, “Distribute skills with plugins”: https://learn.chatgpt.com/docs/build-skills
Codex supports explicit selection and description-based implicit selection. Its initial catalogue can shorten or omit entries under a context budget. Repository, user, admin and system scopes exist. Identically named skills are not merged and can both appear. A plugin can distribute skills together with optional connectors. These are Codex facts, not universal requirements of the open format.

## S6 · Authoring guidance
OpenAI, Build skills, “Create a skill”, “Optional metadata”, “Best practices”: https://learn.chatgpt.com/docs/build-skills
Start instruction-only; add code for deterministic work or external tooling. Keep a skill focused, state inputs and outputs, and test trigger prompts. Codex's optional agents/openai.yaml can disable implicit invocation while preserving explicit selection, and declare tool dependencies.

## S7 · Tool execution
Agent Skills, Using scripts in skills, “One-off commands”, “Referencing scripts”, “Designing scripts for agentic use”: https://agentskills.io/skill-creation/using-scripts
A skill can reference an existing command or bundle a script. The runtime must provide its dependencies. Explicit arguments, useful errors and machine-readable output help an agent execute reliably. Reading a script and executing it are different operations; an invocation still needs its result inspected.

## S8 · Evaluation loop
Agent Skills, Evaluating skill output quality, “Designing test cases”, “Running evals”, “Writing assertions”: https://agentskills.io/skill-creation/evaluating-skills
Evaluate realistic prompts and edge cases against expected outcomes. Compare the same task with the skill and with no skill or its prior version. Independent runs reduce context contamination. Observable assertions and human visual judgment address different qualities; an attractive example alone does not establish general reliability.

## S9 · Conceptual authority boundary
Teaching interpretation derived from S4–S7, not an implementation claim. The model distinguishes user intent, agent interpretation, packaged guidance, host control and execution tools. Instructions guide reasoning; they do not change model weights or themselves authorize an operation. Host permissions, available tools and dependencies remain separate gates. Tool results can be errors; a returned artifact must still be checked.

## S10 · Concrete source-to-model example
Workflow for this Agent Skills study, not a performance measurement or assertion that every acceptance check has passed. The user asks how agent skills work; the source set is the format specification, host documentation and evaluation guidance. Agent selects the skill, reads its method, extracts sourced entities and conditions, and prepares a candidate model. A permitted native checker may accept syntax/relationships or report errors. An HTML builder projects the model into explanatory views. Agent checks source meaning and the delivered interaction before returning source, model and views. If a source changes, regenerate and recheck affected assertions; an old report cannot certify new bytes.

## S11 · Proposed maintenance policy for this teaching system
Derived design, not a mandatory standard. A maintained skill has a draft, a candidate under evaluation, a released baseline and a retired state. Candidate failures return to revision. Release requires recorded evaluation of the same candidate; merely changing the text does not establish improvement. A new revision keeps the previous baseline available until the replacement is evaluated.

## S12 · Open host questions
Host-specific questions remain open unless current host documentation answers them: discovery locations, name collisions, implicit invocation policy, trust checks, capability provisioning and exact permission prompts. The model's responsibility groups describe concepts, not hidden product services or measured timings.
