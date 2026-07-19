from .document import Document
from .html_renderer import HTMLRenderer


class Forge:

    def __init__(self):
        self.document = Document()

    def build(self):

        renderer = HTMLRenderer()

        html = renderer.render(self.document)

        print(html)