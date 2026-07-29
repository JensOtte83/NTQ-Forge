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

Generate a themed SVG diagram and drop it into a figure:

```python
from ntqforge import Figure, relation_diagram, flow_diagram

Figure(svg=relation_diagram(left="ε", right="Δ"), caption="Das Kernsymbol")
Figure(svg=flow_diagram(["Objekt", "Renderer", "HTML"]))
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
- **Prose** — `Heading`, `Text`, `Quote`, `BulletList`, `CodeBlock`, `Divider`, `Badge`, `Log`, `Raw`
- **Diagrams** — `relation_diagram` (ε↔Δ) and `flow_diagram` (horizontal or vertical), built on the `Diagram` canvas

Chapters, figures and tables are numbered automatically (`1`, `1.1`, ... / `Abb. 1` / `Tab. 1`). Numbering is automatic but editable: set `.number` on any component to override its label.

## Markdown import

`from_markdown()` converts any Markdown file into a themed document. Supported: headings (nested chapters), paragraphs with hard line breaks, blockquotes, unordered and ordered lists, fenced code, horizontal rules, and inline **bold**, *italic*, `code` and [links](url). The first H1 becomes the document title.

## Rendering

`HTMLRenderer` produces a full, self-contained HTML5 page in the NTQ design. The theme CSS is inlined and fonts are embedded as base64, so the output — including any generated SVG diagrams — renders identically anywhere with no external files.

The NTQ theme (`themes/ntq/`) provides the design tokens, fonts (DM Mono + Cormorant Garamond), background grid and component styles — a dark, PRM-style aesthetic with an optional light mode.

## Examples

- `examples/theme_demo.py` — the signature layout (panels, formula bar, grid)
- `examples/document_demo.py` — chapters, figures and tables with numbering
- `examples/readme_demo.py` — renders this README in the NTQ design
- `examples/diagram_demo.py` — the ε↔Δ symbol and a render-pipeline flow diagram
- `examples/konzeptpapier_demo.py` — the NTQ-Verse concept paper with the ε↔Δ diagram
- `examples/vision_demo.py` — the NTQ ↔ Vision paper with the reconstruction chain as a vertical diagram

Run any example from the repository root, e.g. `python examples/document_demo.py`, then open the generated file in `dist/`.

## Status & Roadmap

Alpha. The core engine works end to end: a semantic document tree renders to NTQ-themed, self-contained HTML, with a Markdown importer and an SVG diagram engine.

Done so far: HTML renderer, NTQ theme, signature components, structure components with numbering, Markdown import, SVG diagram engine.

Next up: PDF renderer, Markdown export, a network-graph diagram (once the ORK algorithm from the PRM-AI project is ready), and the Vision / PRM / GSRP paper generators.

See [ROADMAP.md](ROADMAP.md) for the full list.

## License

AGPL-3.0. See `LICENSE`.
