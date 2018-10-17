from NegationNode import NegationNode
from VariableNode import VariableNode

from copy import deepcopy as dc

class AndNode:
    solved_nodes = []
    unsolved_nodes = []
    solved_variables = {}

    def __init__(self, child_nodes=[]):
        self.unsolved_nodes = child_nodes

    def add_solved_node(self, node):
        if self.solved_variables.get(str(NegationNode(node)), 0) > 0:
            return True

        self.solved_nodes.append(node)
        str_repr = str(node)
        self.solved_variables[str_repr] = self.solved_variables.get(str_repr, 0) + 1
        return False

    def remove_solved_node(self, node):
        self.solved_nodes.remove(node)
        self.solved_variables[str(node)] -= 1


    def __str__(self):
        to_print = "AND("
        for node in self.solved_nodes:
            to_print += str(node) + ", "
        for node in self.unsolved_nodes:
            to_print += str(node) + ", "
        to_print += ")"
        return to_print

    def deepcopy(self):
        new_node = AndNode()
        new_node.solved_nodes = self.solved_nodes[:]
        new_node.unsolved_nodes = self.unsolved_nodes[:]
        new_node.solved_variables = dc(self.solved_variables)
        return new_node