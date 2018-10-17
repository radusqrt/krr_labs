from parser import GrammarTransformer
from util import stringify
from copy import deepcopy, copy

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
        root = GrammarTransformer().transform(content)

        results = {}
        results['satisfiable'] = False

        self.dfs(root, results)

        if results['satisfiable'] == True:
            print(filename, 'SATISFIABLE', stringify(results['example']))
        else:
            print(filename, 'NON SATISFIABLE')

    def dfs(self, root, results):
        # Stop if satisfiability is found
        if results['satisfiable'] == True:
            return

        # If there are no more unsolved nodes, we found a solution
        if len(root.unsolved_nodes) == 0:
            new_solution = list(map(lambda x: deepcopy(x), root.solved_nodes))
            results['satisfiable'] = True
            results['example'] = new_solution
            return

        # Search for unsolved nodes that create trunks
        for node in root.unsolved_nodes:
            if isinstance(node, VariableNode) or (
                isinstance(node, NegationNode) and isinstance(
                    node.value, VariableNode
                )
            ):
                root.unsolved_nodes.remove(node)
                conflict = root.add_solved_node(node)
                if conflict:
                    return

                self.dfs(root, results)
                return
            elif isinstance(node, AndNode):
                # Try to add node's solved nodes to root
                for solved_node in node.solved_nodes:
                    conflict = root.add_solved_node(solved_node)
                    if conflict:
                        return
                root.unsolved_nodes.remove(node)
                root.unsolved_nodes.extend(node.unsolved_nodes)

                self.dfs(root, results)
                return
            elif isinstance(node, NegationNode) and isinstance(node.value, OrNode):
                root.unsolved_nodes.remove(node)
                root.unsolved_nodes.extend(list(map(lambda x: NegationNode(x), node.value.child_nodes)))

                self.dfs(root, results)
                return
            elif isinstance(node, NegationNode) and isinstance(node.value, ImplicationNode):
                root.unsolved_nodes.remove(node)
                root.unsolved_nodes.append(AndNode([node.value.p, NegationNode(node.value.q)]))
                self.dfs(root, results)
                return

        for node in root.unsolved_nodes:
            if isinstance(node, OrNode):
                for or_node in node.child_nodes:
                    new_root = root.deepcopy()
                    new_root.unsolved_nodes.remove(node)
                    new_root.unsolved_nodes.append(or_node)
                    self.dfs(new_root, results)
                return
            elif isinstance(node, ImplicationNode):
                left_root = root.deepcopy()
                left_root.unsolved_nodes.remove(node)
                left_root.unsolved_nodes.append(NegationNode(node.p))
                self.dfs(left_root, results)

                right_root = root.deepcopy()
                right_root.unsolved_nodes.remove(node)
                right_root.unsolved_nodes.append(node.q)
                self.dfs(right_root, results)
                return
            elif isinstance(node, IffNode):
                left_root = root.deepcopy()
                left_root.unsolved_nodes.remove(node)
                left_root.unsolved_nodes.append(AndNode([node.p, node.q]))
                self.dfs(left_root, results)

                right_root = root.deepcopy()
                right_root.unsolved_nodes.remove(node)
                right_root.unsolved_nodes.append(AndNode(
                    [NegationNode(node.p), NegationNode(node.q)]))
                self.dfs(right_root, results)
                return
            elif isinstance(node, NegationNode) and isinstance(node.value, AndNode):
                for and_node in node.value.solved_nodes + node.value.unsolved_nodes:
                    new_root = root.deepcopy()
                    new_root.unsolved_nodes.remove(node)
                    new_root.unsolved_nodes.append(NegationNode(and_node))
                    self.dfs(new_root, results)
                return
            elif isinstance(node, NegationNode) and isinstance(node.value, IffNode):
                left_root = root.deepcopy()
                left_root.unsolved_nodes.remove(node)
                left_root.unsolved_nodes.append(AndNode([node.p, NegationNode(node.q)]))
                self.dfs(left_root, results)

                right_root = root.deepcopy()
                right_root.unsolved_nodes.remove(node)
                right_root.unsolved_nodes.append(AndNode([NegationNode(node.p), node.q]))
                self.dfs(right_root, results)
                return
            else:
                print("Unknown type of AndNode child")
                return
