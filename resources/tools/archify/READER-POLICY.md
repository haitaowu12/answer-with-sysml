# Subject-led diagram output

The delivered reader explains the subject. It does not advertise the rendering engine or expose production bookkeeping as explanation. This is the package's presentation policy. Keep the upstream attribution, MIT licence, font notices and implementation provenance in the package and source records.

The original subject-led reader patch has three file seams, applied before the engine computes delivery identities:

- `upstream/renderers/shared/i18n.mjs` calls `reader-policy.mjs` for both static and runtime messages. Accessibility descriptions, editorial plates and Route/Reach share-card badges carry no Archify branding. Bundled languages keep their own controls. English selection panels use “Details” and “Follow connections.”
- `upstream/assets/template.html` removes the promotional help link, hides preset stamps (including the decorative “REV 01”), and excludes generic renderer kind/context and internal IDs from the selection panel and Finder. Authored labels, sublabels, tags, sources and relationship actions remain available. Internal semantic attributes and link identities are preserved for interaction.
- The template embeds the retained MIT notice as a non-rendered comment, so the standalone reader carries its attribution without adding promotional UI.
- `upstream/renderers/shared/cli.mjs` omits generic renderer context from node accessibility labels and SVG tooltips. Meaningful authored sublabels remain. SVG and image export use these same generated facts.

Do not rename code identifiers or delete licence notices to hide UI branding. Do not broadly replace words in authored titles or model content: a real explanation about Archify must still be able to name its subject. The policy removes renderer-supplied promotion. User-authored content remains the author's responsibility.

For new explanations, lead with a clear question, diagram and useful takeaway. Keep conditions, material omissions, uncertainty and essential legends visible. Put exact source locations behind source inspection; retain source/model evidence and validation receipts as separate files. Do not add model hashes, transport paths, validator output, implementation plans, production status or repeated proof disclaimers to the main page. Avoid software categories for physical or conceptual systems; select the appropriate typed renderer and meaningful labels.

The ten-type integration tests exercise the shared patch and strict artifact checks; bundled-locale tests cover branded descriptions, presets and share-card message catalogs. Actual exported pixels and interactive states still need browser inspection when affected. A machine check alone does not establish that a page is uncluttered or useful.

The 17 October semantic integration also marks lifecycle final borders explicitly so a scoped SysML adapter can remove inferred final-state notation. The reader template respects an optional inspect-only traversal policy and exposes validated camera restoration. The local model-session service is host implementation, not an Archify modeling engine.

During a donor refresh, diff all four modified production files against the pin, retain this policy module beside `upstream/`, reconcile equivalent upstream behavior, and rerun the affected reader and export checks. Do not report the vendor tree as pristine. Directly opening old generated files does not apply this policy: regenerate from their editable source.

