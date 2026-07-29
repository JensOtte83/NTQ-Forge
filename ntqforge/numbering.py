"""
NTQ Forge

Numbering.

Walks a document tree once and assigns numbers to numbered components
(:class:`~ntqforge.components.Chapter`, :class:`~ntqforge.components.Figure`,
:class:`~ntqforge.components.Table`).

Rules
-----
- Chapters are numbered hierarchically by nesting depth: 1, 1.1, 1.1.1, 2 ...
- Figures and tables are numbered sequentially in reading order,
  document-wide: 1, 2, 3 ...
- The counter always advances for every item of a type, so ordinals stay
  stable. What gets *displayed* is the manual override if one was set
  (``component.number``), otherwise the computed value. That is what makes
  numbering "automatic but editable afterwards": set ``.number`` on any
  component to override its label; leave it ``None`` for the auto value.

This function is called automatically by the HTML renderer before
rendering, so callers normally never invoke it directly. It is idempotent:
running it again simply recomputes the automatic numbers.
"""


def assign_numbers(root):
    """Assign ``_computed_number`` (and chapter ``level``) across the tree."""
    # Local import avoids a circular import at module load time.
    from .components import Chapter, Figure, Table

    counters = {"figure": 0, "table": 0}

    def children_of(node):
        # Both Document and Component are iterable over their children.
        try:
            return list(node)
        except TypeError:
            return []

    def visit(node, chapter_prefix):
        chapter_index = 0
        for child in children_of(node):
            if isinstance(child, Chapter):
                chapter_index += 1
                number_parts = chapter_prefix + [str(chapter_index)]
                child._computed_number = ".".join(number_parts)
                child.level = len(number_parts)
                # Nesting uses the computed numeric prefix even if this
                # chapter's own label was overridden, so children stay sane.
                visit(child, number_parts)
            elif isinstance(child, Figure):
                counters["figure"] += 1
                child._computed_number = str(counters["figure"])
                visit(child, chapter_prefix)
            elif isinstance(child, Table):
                counters["table"] += 1
                child._computed_number = str(counters["table"])
                visit(child, chapter_prefix)
            elif hasattr(child, "children"):
                # Any other container component (Panel, Grid, ...).
                visit(child, chapter_prefix)
            # plain strings and leaf components: nothing to number

    visit(root, [])
    return root
