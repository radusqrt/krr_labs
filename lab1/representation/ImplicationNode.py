from NegationNode import NegationNode
from OrNode import OrNode

class ImplicationNode:
    p = None
    q = None

    def __init__(self, p, q):
        self.p = p
        self.q = q

    def __str__(self):
        to_print = "IMPL(" + str(self.p) + ", " + str(self.q) + ")"
        return to_print
