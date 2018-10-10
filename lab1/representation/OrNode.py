class OrNode:
    child_nodes = []

    def __init__(self, child_nodes=[]):
        self.child_nodes = child_nodes

    def __str__(self):
        to_print = "OR("
        for node in self.child_nodes:
            to_print += str(node) + ", "
        to_print += ")"
        return to_print
