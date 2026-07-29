"""
NTQ Forge

Renderer base class.

A Renderer turns a Document (a tree of Components) into an output format.
Concrete renderers (HTML, PDF, SVG) implement :meth:`render`.

The base provides :meth:`render_children`, the recursive walk used by
components: Components are rendered via their own ``render`` method, plain
strings are passed through as raw markup.
"""


class Renderer:
    """Abstract renderer."""

    def render(self, document):
        raise NotImplementedError(
            f"{type(self).__name__} does not implement render()"
        )

    def render_children(self, children):
        """Render an iterable of children to a single string.

        - Component  -> ``child.render(self)``
        - str        -> passed through unchanged (raw markup)
        - other      -> ``str(child)``
        """
        out = []
        for child in children:
            if hasattr(child, "render") and callable(child.render):
                out.append(child.render(self))
            else:
                out.append(str(child))
        return "\n".join(part for part in out if part)
