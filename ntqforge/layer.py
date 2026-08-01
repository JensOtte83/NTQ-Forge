"""
NTQ ↔ Forge

Layer

Ein Layer definiert genau eine rekonstruktive
Unterscheidung.

Ein Layer besitzt keine Kenntnis über
Netzwerke oder Stacks.

Er transformiert ausschließlich den
aktuellen Zustand.
"""


class Layer:

    def run(self, data):
        return data
