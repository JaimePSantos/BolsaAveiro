from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,TT_INTERVALVAR,TT_PROGTEST, TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN

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

class TestNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
      return f'({self.element_nodes})'

class BoxPropNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
      elementStr = str(self.element_nodes)[1:-1]
      return f'([{{{elementStr}}}])'

class DiamondPropNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
      elementStr = str(self.element_nodes)[1:-1]
      return f'(<{{{elementStr}}}>)'

class ParenthesisNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
    def __repr__(self):
      elementStr = str(self.element_nodes)[1:-1]
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
        #print("Prog: "+str(self.left_node) + " " + str(self.op_tok) + " " + str(self.right_node) )
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