from .renderer import Renderer


class HTMLRenderer(Renderer):

    def render(self, document):

        html = "<html>\n"

        html += f"<h1>{document.title}</h1>\n"

        for component in document:

            html += component.render(self)

        html += "</html>"

        return html