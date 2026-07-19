class Document:

    def __init__(self):

        self.title = "Untitled"

        self.components = []

    def add(self, component):

        self.components.append(component)