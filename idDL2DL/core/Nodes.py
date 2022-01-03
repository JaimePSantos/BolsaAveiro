from idDL2DL.core.Tokens import TT_INTERVALPLUS, \
    TT_INTERVALMULT, TT_GEQ, TT_SEQ, TT_GT, TT_ST, TT_NOT, TT_AND, TT_PROGTEST, TT_PROGAND, TT_PROGUNION, \
    TT_PROGSEQUENCE, TT_PROGASSIGN


#######################################
# NODES
#######################################

class LowerNumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class UpperNumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class IntervalVarNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class DifferentialVarNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class SeparatorNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class BoxNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'({{{self.element_nodes}}})'


class DiamondNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'({self.element_nodes})'


class BoxPropNode:
    def __init__(self, element_nodes, boxProp, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.boxProp = boxProp

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        boxPropStr = str(self.boxProp)[1:-1]
        return f'([{{{elementStr}}}],{boxPropStr})'


class ForallPropNode:
    def __init__(self, element_nodes, forallProp, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.forallProp = forallProp

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        forallPropStr = str(self.forallProp)[1:-1]
        return f'([{{{elementStr}}}],{forallPropStr})'


class DiamondPropNode:
    def __init__(self, element_nodes, diamondProp, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.diamondProp = diamondProp

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        diamondPropStr = str(self.diamondProp)[1:-1]
        return f'(<{{{elementStr}}}>,{diamondPropStr})'


class ParenthesisNode:
    def __init__(self, element_nodes, pos_start, pos_end, zeroAryNode=None):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        if zeroAryNode is not None:
            self.zeroAryNode = zeroAryNode

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        if self.zeroAryNode is not None:
            zAryElementStr = str(self.zeroAryNode)[1:-1]
            return f'(({elementStr}){zAryElementStr})'
        else:
            return f'({elementStr})'


class CurlyParenthesisNode:
    def __init__(self, element_nodes, pos_start, pos_end, zeroAryNode=None):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
        if zeroAryNode is not None:
            self.zeroAryNode = zeroAryNode

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        if self.zeroAryNode is not None:
            zAryElementStr = str(self.zeroAryNode)[1:-1]
            return f'{{{elementStr}{zAryElementStr}}}'
        else:
            return f'({elementStr})'


class TestProgNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        elementStr = str(self.element_nodes)[1:-1]
        return f'({elementStr})'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class PropOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end
        # print("Prog: "+str(self.left_node) + " " + str(self.op_tok) + " " + str(self.right_node) )

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class ProgOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class ProgDifNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class ZeroAryNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class UnaryProgOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class UnaryForallOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


#######################################
# PrettyNODES
#######################################

class PrettyLowerNumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok.value}'


class PrettyUpperNumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok.value}'


class PrettyIntervalNode:
    tokList = []

    def __init__(self, tokList):
        self.tokList = tokList

    def __repr__(self):
        return f'{self.tokList}'


class PrettySeparatorNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = ', '
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'[{self.left_node} {self.op_tok} {self.right_node}]'


class PrettyBinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        if op_tok.type in TT_INTERVALPLUS:
            self.op_tok = '+'
        elif op_tok.type in TT_INTERVALMULT:
            self.op_tok = '*'
        elif op_tok.type in TT_SEQ:
            self.op_tok = '<='
        elif op_tok.type in TT_GEQ:
            self.op_tok = '>='
        elif op_tok.type in TT_ST:
            self.op_tok = '<'
        elif op_tok.type in TT_GT:
            self.op_tok = '>'
        else:
            self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'( {self.left_node} {self.op_tok} {self.right_node} )'


class PrettyPropOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        if op_tok.type in TT_AND:
            self.op_tok = '∧'
        else:
            self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'{self.left_node} {self.op_tok} {self.right_node}'


class PrettyUnaryOpNode:
    def __init__(self, op_tok, node):
        if op_tok.type in TT_NOT:
            self.op_tok = '¬'
        elif op_tok.type in TT_PROGTEST:
            self.op_tok = '?'
        else:
            self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f' {self.op_tok} ( {self.node} )'


class PrettyIntervalVarNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok.value}'


class PrettyProgOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        if op_tok.type in TT_PROGAND:
            self.op_tok = '&'
        elif op_tok.type in TT_PROGUNION:
            self.op_tok = '∪'
        elif op_tok.type in TT_PROGSEQUENCE:
            self.op_tok = '∘'
        elif op_tok.type in TT_PROGASSIGN:
            self.op_tok = ':='

        else:
            self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f' {self.left_node} {self.op_tok} {self.right_node} '
