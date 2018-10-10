from copy import deepcopy

from NegationNode import NegationNode
from VariableNode import VariableNode

class AndNode:
    solved_nodes = []
    unsolved_nodes = []

    def __init__(self, child_nodes=[]):
        self.solved_nodes = []
        self.unsolved_nodes = child_nodes

    def surely_not_satisfiable(self):
        for node_1 in self.solved_nodes:
            for node_2 in self.solved_nodes:
                if isinstance(
                        node_1,
                        VariableNode) and isinstance(
                        node_2,
                        NegationNode) and node_1.name == node_2.value.name:
                    return True
                if isinstance(
                        node_2,
                        VariableNode) and isinstance(
                        node_1,
                        NegationNode) and node_2.name == node_1.value.name:
                    return True
        return False

    def __str__(self):
        to_print = "AND("
        for node in self.solved_nodes:
            to_print += str(node) + ", "
        for node in self.unsolved_nodes:
            to_print += str(node) + ", "
        to_print += ")"
        return to_print
