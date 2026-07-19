"""
NTQ Forge

Semantic document root.
"""

from dataclasses import dataclass, field


@dataclass
class Document:

    title: str = ""

    author: str = ""

    language: str = "en"

    children: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


    def add(self, element):

        self.children.append(element)

        return element


    def extend(self, elements):

        self.children.extend(elements)

        return self


    def __iter__(self):

        return iter(self.children)