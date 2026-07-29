# NTQ Forge

> Open-Source document generation engine for PRM, GSRP and technical publications.

NTQ Forge is a Python framework for generating structured technical documents from reusable, semantic components. Instead of hand-writing HTML, documents are built from objects such as chapters, figures, tables and diagrams, then rendered — currently to self-contained HTML in the NTQ design.

## Philosophy

NTQ Forge follows the same architectural principles as the PRM ecosystem.

- **Clear Boundaries** — each component owns a single concern
- **Reusable Components** — documents are built from objects, not markup
- **Renderer Independence** — the same document tree can target different output formats
- **Open Science** — readable, inspectable input and output
- **Local First** — no network required; rendered output is fully self-contained

## Quickstart

```python
from ntqforge import Document, Forge, Chapter, Text, Table

doc = Document(
    title="PRM",
    metadata={"subtitle": "Perspektivisches Referenzpunkt Modell", "accent": "R"},
)

intro = Chapter("Introduction")
intro.add(Text("Documents are built from semantic objects."))
doc.add(intro)

doc.add(Table(
    headers=["Component", "Purpose"],
    rows=[["Chapter", "Numbered sections"], ["Figure", "Image or SVG + caption"]],
    caption="Core components.",
))

Forge(doc).build("dist/index.html")
```

Any Markdown file (a README, notes, a draft) can be rendered in the NTQ design:

```python
from ntqforge import Forge, from_markdown

doc = from_markdown(open("README.md").read(), subtitle="rendered by NTQ Forge")
Forge(doc).build("dist/readme.html")
```

## Components

- **Structure** — `Document`, `Chapter` (hierarchical), `Figure` (image or inline SVG + caption), `Table`
- **Layout** — `Panel`, `FormulaBar`, `Grid` — the PRM signature layout
- **Prose** — `Heading`, `Text`, `Quote`, `BulletList`, `CodeBlock`, `Badge`, `Log`, `Raw`

Chapters, figures and tables are numbered automatically (`1`, `1.1`, ... / `Abb. 1` / `Tab. 1`). Numbering is automatic but editable: set `.number` on any component to override its label.

## Rendering

`HTMLRenderer` produces a full, self-contained HTML5 page in the NTQ design. The theme CSS is inlined and fonts are embedded as base64, so the output renders identically anywhere with no external files.

The NTQ theme (`themes/ntq/`) provides the design tokens, fonts (DM Mono + Cormorant Garamond), background grid and component styles — a dark, PRM-style aesthetic with an optional light mode.

## Roadmap

- ✓ HTML renderer
- ✓ NTQ design theme
- ✓ Signature components (Panel / FormulaBar / Grid)
- ✓ Structure components (Chapter / Figure / Table) with automatic numbering
- ✓ Markdown import (`from_markdown`)
- ○ SVG diagram engine
- ○ PDF renderer
- ○ Markdown export
- ○ Vision / PRM / GSRP paper generators

## Examples

- `examples/theme_demo.py` — the signature layout (panels, formula bar, grid)
- `examples/document_demo.py` — chapters, figures and tables with numbering
- `examples/readme_demo.py` — renders this README in the NTQ design

Run any example from the repository root, e.g. `python examples/document_demo.py`, then open the generated file in `dist/`.

## Status

Alpha. The core engine works end to end: a semantic document tree renders to NTQ-themed, self-contained HTML. The diagram engine, PDF output and the paper generators are still to come.

## License

AGPL-3.0. See `LICENSE`.
