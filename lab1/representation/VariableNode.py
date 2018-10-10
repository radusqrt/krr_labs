class VariableNode:
    name = None

    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        to_print = "VAR(" + str(self.name) + ")"
        return to_print
