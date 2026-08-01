"""
NTQ Forge

Open-Source document generation engine for PRM, GSRP and technical
publications.

Public API
----------
    from ntqforge import Forge, Document, Theme
    from ntqforge import Panel, FormulaBar, Grid, Heading, Text, Raw
"""
from .layer import Layer
from .stack import Stack
from .network import Network
from .document import Document
from .theme import Theme
from .renderer import Renderer
from .html_renderer import HTMLRenderer
from .forge import Forge

from .components import (
    Panel,
    FormulaBar,
    Grid,
    Heading,
    Text,
    Raw,
    Badge,
    Log,
    Chapter,
    Figure,
    Table,
    Quote,
    BulletList,
    CodeBlock,
    Divider,
)
from .markdown_import import from_markdown
from .diagram import Diagram, relation_diagram, flow_diagram

__version__ = "0.1.0"

__all__ = [
    "Forge",
    "Layer",
    "Stack",
    "Network",
    "Document",
    "Theme",
    "Renderer",
    "HTMLRenderer",
    "Panel",
    "FormulaBar",
    "Grid",
    "Heading",
    "Text",
    "Raw",
    "Badge",
    "Log",
    "Chapter",
    "Figure",
    "Table",
    "Quote",
    "BulletList",
    "CodeBlock",
    "Divider",
    "from_markdown",
    "Diagram",
    "relation_diagram",
    "flow_diagram",
    "__version__",
]
