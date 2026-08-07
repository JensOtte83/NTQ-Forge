"""
NTQ Forge — App Launcher

Erzeugt die NTQ-Forge Startseite im NTQ-Theme.
"""

from pathlib import Path
import webbrowser

from ntqforge import (
    Badge,
    Document,
    Forge,
    Grid,
    Heading,
    HTMLRenderer,
    Log,
    Panel,
    Text,
)


def build():

    doc = Document(
        title="NTQ FORGE",
        metadata={
            "subtitle": "Boundary • Relation • Delta",
            "accent": "NTQ",
        },
    )

    doc.add(
        Grid(

            Panel(
                Heading("CREATE"),
                Text("Create datasets, layers and structures."),
                Badge("READY", accent="success"),
                title="Module . CREATE",
            ),

            Panel(
                Heading("ANALYZE"),
                Text("Run delta_core and relation pipelines."),
                Badge("READY", accent="info"),
                title="Module . ANALYZE",
            ),

            Panel(
                Heading("TRAIN"),
                Text("Train models, characters and memories."),
                Badge("COMING SOON", accent="warning"),
                title="Module . TRAIN",
            ),

            Panel(
                Heading("EXPERIMENT"),
                Text("Prototype new ideas and pipelines."),
                Badge("LAB", accent="danger"),
                title="Module . EXPERIMENT",
            ),

            columns=2,
        )
    )

    doc.add(

        Panel(
            Heading("Status"),

            Log(
                entries=[
                    ("NTQ Theme loaded", "success"),
                    ("Forge initialized", "success"),
                    ("delta_core: waiting", "info"),
                    ("Status: Ready", "success"),
                ]
            ),

            title="System",
            accent="success",
        )

    )

    return doc


def main():

    output = Path("dist")
    output.mkdir(exist_ok=True)

    outfile = output / "index.html"

    forge = Forge(
        build(),
        renderer=HTMLRenderer(embed_fonts=True),
    )

    forge.build(str(outfile))

    webbrowser.open(outfile.resolve().as_uri())


if __name__ == "__main__":
    main()
