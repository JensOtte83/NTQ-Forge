"""
NTQ Forge

Markdown import.

``from_markdown(text)`` converts a Markdown string into a
:class:`~ntqforge.document.Document` built from NTQ Forge components, so any
Markdown file (a README, notes, a draft) can be rendered in the NTQ design.

Supported block elements: ATX headings (``#`` … ``######``), paragraphs,
blockquotes, unordered lists (``-``, ``*``, ``+``), ordered lists
(``1.``), and fenced code blocks (```` ``` ````). Supported inline
elements: ``**bold**``, ``*italic*`` / ``_italic_``, ``inline code`` and
``[links](url)``.

Headings build a nested :class:`~ntqforge.components.Chapter` tree by
level. The first level-1 heading becomes the document title unless a
``title`` is passed. Chapter numbering is off by default (README style);
pass ``numbered=True`` for an auto-numbered document.
"""

import html
import re

from .document import Document
from .components import Chapter, Text, Quote, BulletList, CodeBlock, Divider


# -- inline formatting ---------------------------------------------------

_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)|_([^_]+)_")


def inline(text):
    """Escape ``text`` and apply inline Markdown → HTML."""
    out = html.escape(text, quote=False)
    # inline code first, so its contents are not further formatted
    out = _CODE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    out = _LINK.sub(
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">'
                  f"{m.group(1)}</a>",
        out,
    )
    out = _BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = _ITALIC.sub(
        lambda m: f"<em>{m.group(1) if m.group(1) else m.group(2)}</em>", out
    )
    return out


# -- block parsing -------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_ULIST = re.compile(r"^[-*+•·]\s+(.*)$")
_OLIST = re.compile(r"^\d+[.)]\s+(.*)$")
_QUOTE = re.compile(r"^>\s?(.*)$")
_FENCE = re.compile(r"^```(.*)$")


def from_markdown(text, title=None, numbered=False, **metadata):
    """Convert a Markdown string into a themed :class:`Document`."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    doc = Document(metadata=dict(metadata))
    # chapter stack: list of (level, chapter); target is the innermost
    stack = []

    def current_container():
        return stack[-1][1] if stack else doc

    def add_block(component):
        current_container().add(component)

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # blank line
        if not line.strip():
            i += 1
            continue

        # fenced code block
        fence = _FENCE.match(line)
        if fence:
            lang = fence.group(1).strip() or None
            code_lines = []
            i += 1
            while i < n and not _FENCE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            add_block(CodeBlock("\n".join(code_lines), language=lang))
            continue

        # horizontal rule (---, ***, ___, also spaced) — before lists,
        # so "- - -" is a rule, not a list item.
        compact = line.strip().replace(" ", "")
        if len(compact) >= 3 and len(set(compact)) == 1 and compact[0] in "-*_":
            add_block(Divider())
            i += 1
            continue

        # heading
        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            htext = heading.group(2).strip()

            # first H1 becomes the document title (unless one was given)
            if level == 1 and title is None and not doc.title and not stack:
                doc.title = htext
                title = htext
                i += 1
                continue

            # pop to the correct parent depth
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent = current_container()
            chapter = Chapter(htext, number=None if numbered else "")
            parent.add(chapter)
            stack.append((level, chapter))
            i += 1
            continue

        # blockquote (consecutive)
        if _QUOTE.match(line):
            quote_lines = []
            while i < n and _QUOTE.match(lines[i]):
                quote_lines.append(_QUOTE.match(lines[i]).group(1))
                i += 1
            add_block(Quote(inline(" ".join(quote_lines)), raw=True))
            continue

        # unordered list (consecutive)
        if _ULIST.match(line):
            items = []
            while i < n and _ULIST.match(lines[i]):
                items.append(inline(_ULIST.match(lines[i]).group(1)))
                i += 1
            add_block(BulletList(items, raw=True))
            continue

        # ordered list (consecutive)
        if _OLIST.match(line):
            items = []
            while i < n and _OLIST.match(lines[i]):
                items.append(inline(_OLIST.match(lines[i]).group(1)))
                i += 1
            add_block(BulletList(items, ordered=True, raw=True))
            continue

        # paragraph (consecutive non-blank, non-special lines).
        # Hard line breaks are preserved (joined with <br>), so
        # hand-authored line structure (e.g. definition blocks) survives.
        para_lines = []
        while i < n and lines[i].strip() and not (
            _HEADING.match(lines[i]) or _ULIST.match(lines[i])
            or _OLIST.match(lines[i]) or _QUOTE.match(lines[i])
            or _FENCE.match(lines[i])
        ):
            para_lines.append(lines[i].strip())
            i += 1
        add_block(Text("<br>".join(inline(l) for l in para_lines), raw=True))

    if title is not None and not doc.title:
        doc.title = title
    return doc
