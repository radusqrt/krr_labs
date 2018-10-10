from parser import GrammarTransformer
from util import stringify
from copy import deepcopy

from representation.AndNode import AndNode
from representation.OrNode import OrNode
from representation.ImplicationNode import ImplicationNode
from representation.IffNode import IffNode
from representation.NegationNode import NegationNode
from representation.VariableNode import VariableNode

class SemanticTableaux:

    def solve(self, filename):
        with open(filename, 'r') as content_file:
            content = content_file.read()
        second = GrammarTransformer().transform(content)

        results = {}
        results['satisfiable'] = False

        self.dfs(second, results)

        if results['satisfiable'] == True:
            print(filename, 'SATISFIABLE', stringify(results['example']))
        else:
            print(filename, 'NON SATISFIABLE')

    def dfs(self, root, results):
        if results['satisfiable'] == True:
            return
        if (root.surely_not_satisfiable()):
            return
        if len(root.unsolved_nodes) == 0:
            new_solution = list(map(lambda x: deepcopy(x), root.solved_nodes))
            results['satisfiable'] = True
            results['example'] = new_solution
            return
        visited = []
        for node in root.unsolved_nodes:
            if node in visited:
                continue
            visited.append(node)
            if isinstance(node, VariableNode) or (
                isinstance(node, NegationNode) and isinstance(
                    node.value, VariableNode
                )
            ):
                root.unsolved_nodes.remove(node)
                root.solved_nodes.append(node)
                self.dfs(root, results)

                root.solved_nodes.remove(node)
                root.unsolved_nodes.append(node)
            elif isinstance(node, AndNode):
                root.unsolved_nodes.remove(node)
                root.unsolved_nodes.extend(node.unsolved_nodes)
                root.solved_nodes.extend(node.solved_nodes)
                self.dfs(root, results)

                root.unsolved_nodes.append(node)
                for unsolved_node in node.unsolved_nodes:
                    root.unsolved_nodes.remove(unsolved_node)
                for solved_node in node.solved_nodes:
                    root.solved_nodes.remove(solved_node)
            elif isinstance(node, OrNode):
                for or_node in node.child_nodes:
                    root.unsolved_nodes.remove(node)
                    root.unsolved_nodes.append(or_node)
                    self.dfs(root, results)

                    root.unsolved_nodes.remove(or_node)
                    root.unsolved_nodes.append(node)
            elif isinstance(node, ImplicationNode):
                root.unsolved_nodes.remove(node)
                neg_p = NegationNode(node.p)
                root.unsolved_nodes.append(neg_p)
                self.dfs(root, results)

                root.unsolved_nodes.append(node)
                root.unsolved_nodes.remove(neg_p)

                root.unsolved_nodes.remove(node)
                root.unsolved_nodes.append(node.q)
                self.dfs(root, results)

                root.unsolved_nodes.append(node)
                root.unsolved_nodes.remove(node.q)
            elif isinstance(node, IffNode):
                root.unsolved_nodes.remove(node)
                p_and_q = AndNode([node.p, node.q])
                root.unsolved_nodes.append(p_and_q)
                self.dfs(root, results)

                root.unsolved_nodes.append(node)
                root.unsolved_nodes.remove(p_and_q)

                root.unsolved_nodes.remove(node)
                non_p_and_non_q = AndNode(
                    [NegationNode(node.p), NegationNode(node.q)])
                root.unsolved_nodes.append(non_p_and_non_q)
                self.dfs(root, results)

                root.unsolved_nodes.append(node)
                root.unsolved_nodes.remove(non_p_and_non_q)
            elif isinstance(node, NegationNode):
                if isinstance(node.value, AndNode):
                    for and_node in node.value.solved_nodes:
                        root.unsolved_nodes.remove(node)
                        neg_node = NegationNode(and_node)
                        root.unsolved_nodes.append(neg_node)
                        self.dfs(root, results)

                        root.unsolved_nodes.append(node)
                        root.unsolved_nodes.remove(neg_node)
                    for and_node in node.value.unsolved_nodes:
                        root.unsolved_nodes.remove(node)
                        neg_node = NegationNode(and_node)
                        root.unsolved_nodes.append(NegationNode(and_node))
                        self.dfs(root, results)

                        root.unsolved_nodes.append(node)
                        root.unsolved_nodes.remove(neg_node)
                elif isinstance(node.value, OrNode):
                    root.unsolved_nodes.remove(node)
                    neg_nodes = []
                    for or_node in node.value.child_nodes:
                        neg_node = NegationNode(or_node)
                        neg_nodes.append(neg_node)
                        root.unsolved_nodes.append(neg_node)
                    self.dfs(root, results)

                    root.unsolved_nodes.append(node)
                    for neg_node in neg_nodes:
                        root.unsolved_nodes.remove(neg_node)
                elif isinstance(node.value, ImplicationNode):
                    root.unsolved_nodes.remove(node)
                    root.unsolved_nodes.append(node.value.p)
                    neg_q = NegationNode(node.value.q)
                    root.unsolved_nodes.append(neg_q)
                    self.dfs(root, results)

                    root.unsolved_nodes.append(node)
                    root.unsolved_nodes.remove(node.value.p)
                    root.unsolved_nodes.remove(neg_q)
                elif isinstance(node.value, IffNode):
                    root.unsolved_nodes.remove(node)
                    and_node = AndNode([
                        node.value.p, NegationNode(node.value.q)
                    ])
                    root.unsolved_nodes.append(and_node)
                    self.dfs(root, results)

                    root.unsolved_nodes.append(node)
                    root.unsolved_nodes.remove(and_node)

                    root.unsolved_nodes.remove(node)
                    and_node = AndNode([
                        NegationNode(node.value.p), node.value.q
                    ])
                    root.unsolved_nodes.append(and_node)
                    self.dfs(root, results)

                    root.unsolved_nodes.append(node)
                    root.unsolved_nodes.remove(and_node)
                else:
                    print("Unknown type of NegationNode value")
            else:
                print("Unknown type of AndNode child")