"""
NTQ Forge

Component base class.

A Component is a semantic building block of a Document. It knows how to
render itself for a given renderer. Components may contain child
components (or raw strings), which the renderer walks recursively.

The contract is deliberately renderer-agnostic: a Component does not know
*how* it becomes HTML/PDF/SVG, it only asks the renderer to render its
children and assembles the result.
"""

from html import escape as _escape


class Component:
    """Base class for all semantic components."""

    def __init__(self, *children):
        # children may be Components or plain strings (raw markup / text)
        self.children = list(children)

    # -- tree building ------------------------------------------------

    def add(self, child):
        """Append a child and return it (for chaining)."""
        self.children.append(child)
        return child

    def extend(self, children):
        """Append multiple children and return self."""
        self.children.extend(children)
        return self

    def __iter__(self):
        return iter(self.children)

    # -- rendering ----------------------------------------------------

    def render(self, renderer):
        """Render this component for the given renderer.

        Concrete components override this. The default raises, so an
        abstract component used by mistake fails loudly instead of
        silently emitting nothing.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not implement render()"
        )

    # -- helpers ------------------------------------------------------

    @staticmethod
    def escape(text):
        """HTML-escape a value (safe for text nodes and attributes)."""
        return _escape(str(text), quote=True)
