"""
NTQ ↔ Forge

Network

Ein Netzwerk besteht aus
beliebig vielen Stacks.

Das Netzwerk kennt weder
Dateiformate noch Layer.

Es organisiert ausschließlich
Stacks.
"""


class Network:

    def __init__(self):
        self.stacks = []

    def add(self, stack):
        self.stacks.append(stack)

    def remove(self, stack):
        self.stacks.remove(stack)

    def clear(self):
        self.stacks.clear()

    def __len__(self):
        return len(self.stacks)

    def __iter__(self):
        return iter(self.stacks)

    def __repr__(self):
        return f"Network({len(self.stacks)} stacks)"
