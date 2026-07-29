# NTQ Forge — Roadmap

> Status: Alpha. The core engine renders semantic documents to self-contained, NTQ-themed HTML.

This file tracks where NTQ Forge is and where it is going. It is itself renderable via `from_markdown`.

## Done

- **HTML renderer** — full self-contained HTML5 page; theme CSS inlined, fonts embedded as base64
- **NTQ design theme** — tokens, fonts, background grid, component styles, light and dark
- **Signature components** — `Panel`, `FormulaBar`, `Grid`
- **Structure components** — `Chapter`, `Figure`, `Table` with automatic, overridable numbering
- **Prose components** — `Heading`, `Text`, `Quote`, `BulletList`, `CodeBlock`, `Divider`, `Badge`, `Log`, `Raw`
- **Markdown import** — `from_markdown()`: headings, lists, quotes, code, horizontal rules, hard line breaks, inline formatting
- **SVG diagram engine** — `Diagram` canvas plus `relation_diagram` (ε↔Δ) and `flow_diagram` (horizontal / vertical)
- **Real documents** — the README and the NTQ-Verse & NTQ ↔ Vision concept papers all render through NTQ Forge, with generated diagrams

## Next

- **PDF renderer** — the same document tree, rendered to PDF
- **Markdown export** — write documents back out as Markdown (the reverse of the importer)
- **Network-graph diagram** — the reconstruction network (Referenzpunkte · ORKs · Δ · Stacks) as a generated diagram. Waits on a fully working ORK algorithm from the PRM-AI project.
- **Paper generators** — Vision / PRM / GSRP paper builders under `papers/`

## Later / ideas

- **Freeze / Thaw snapshots** — persist and reopen a reconstruction state (per the Vision paper)
- **3D network navigation** — navigate complex reconstructive spaces
- **Additional themes** — beyond the NTQ design

## Legend

- ✓ done · ○ planned
- The double arrow ε ↔ Δ marks the ecosystem identity: relation, analysis, transformation.
