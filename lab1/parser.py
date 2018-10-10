from lark import Lark, Transformer

from representation.ImplicationNode import ImplicationNode
from representation.VariableNode import VariableNode
from representation.AndNode import AndNode
from representation.OrNode import OrNode
from representation.IffNode import IffNode
from representation.NegationNode import NegationNode

grammar = """
    start: aff  -> alias_start

    aff: "NOT" aff              -> neg_func
        | "IF" aff "THEN" aff   -> if_func
        | aff "OR" aff          -> or_func
        | aff "AND" aff         -> and_func
        | aff "IFF" aff         -> iff_func
        | p                     -> prop_func

    p: word+    -> prop

    word: /[a-zA-Z][a-z]+/

    %import common.WS
    %ignore /\./
    %ignore WS
"""

parser = Lark(grammar)

class MyTransformer(Transformer):
    def alias_start(self, value):
        return AndNode(value)

    def and_func(self, value):
        return AndNode(value)

    def if_func(self, value):
        return ImplicationNode(value[0], value[1])

    def iff_func(self, value):
        return IffNode(value[0], value[1])

    def neg_func(self, value):
        return NegationNode(value[0])

    def or_func(self, value):
        return OrNode(value)

    def prop(self, value):
        return VariableNode(' '.join([str(x.children[0]) for x in value]).lower())

    def prop_func(self, value):
        return value[0]

    def end_of_sentence_func(self, value):
        return value[0]

class GrammarTransformer:
    def transform(self, s):
        return AndNode([MyTransformer().transform(parser.parse(line)) for line in s.split('\n') if len(line) > 0])