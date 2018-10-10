from VariableNode import VariableNode

class NegationNode:
    value = None

    def __init__(self, value):
        if isinstance(value, NegationNode):
            self.__class__ = VariableNode
            self.name = value.value.name
        else:
            self.value = value

    def __str__(self):
        to_print = "~" + str(self.value)
        return to_print
