"""
NTQ ↔ Forge

Stack

Ein Stack besteht aus:

- beliebig vielen Layern
- genau einem delta_core (indirekt über seine Layer)

Der Stack kennt weder Dateiformate
noch Renderer.

Er führt seine Layer lediglich
nacheinander aus.
"""


class Stack:

    def __init__(self, *layers):
        self.layers = list(layers)

    def run(self, data):

        state = data

        for layer in self.layers:
            state = layer.run(state)

        return state

    def add(self, layer):
        self.layers.append(layer)

    def clear(self):
        self.layers.clear()

    def __len__(self):
        return len(self.layers)

    def __iter__(self):
        return iter(self.layers)

    def __repr__(self):
        return f"Stack({len(self.layers)} layer)"
