from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV
from Errors import InvalidSyntaxError

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.intervalExpr()
        if not res.error and self.current_tok.type != TT_EOF:
            failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                     "Expected an interval operation."))
            return failure
        return res

    ################################################

    def intervalFactor(self):
        res = ParseResult()
        if self.current_tok.type in TT_LOWERLIM:
            res.register(self.advance())
            success = res.success(LowerNumberNode(self.current_tok))
            res.register(self.advance())
            return success

        if self.current_tok.type in TT_INT:
            tokTemp = self.current_tok
            res.register(self.advance())
            if self.current_tok.type in TT_UPPERLIM:
                success = res.success(UpperNumberNode(tokTemp))
                res.register(self.advance())
                return success

        failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                 "Expected an interval or interval operation ( - or /)."))
        return failure


    def interval(self):
        return self.bin_op(self.intervalFactor, TT_SEPARATOR, True)

    def intervalExpr(self):
        return self.bin_op(self.interval, (TT_INTERVALPLUS, TT_INTERVALMULT))

    ###################################

    def bin_op(self, func, ops,Separator = None):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            if Separator:
                left = SeparatorNode(left, op_tok, right)
            else:
                left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def separator(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = SeparatorNode(left, op_tok, right)
        return res.success(left)

#######################################
# Interpreter
#######################################

class Interpreter:
    def visit(self,node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self,method_name,self.no_visit_method)
        return method(node)

    def no_visit_method(self,node):
        raise Exception(f'No visit_{type(node).__name__} defined.')

    def visit_LowerNumberNode(self,node):
        print("Found LowerNumberNode")

    def visit_UpperNumberNode(self, node):
        print("Found UpperNumberNode")

    def visit_BinOpNode(self, node):
        print("Found BinOpNode")
        self.visit(node.left_node)
        self.visit(node.right_node)

    def visit_SeparatorNode(self, node):
        print("Found SeperatorNode")
        self.visit(node.left_node)
        self.visit(node.right_node)

#######################################
# PARSERESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

#######################################
# NODES
#######################################

class LowerNumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class UpperNumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class IntervalNode:
    tokList = []
    def __init__(self,tokList):
        self.tokList = tokList

    def __repr__(self):
        return f'{self.tokList}'

class SeparatorNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
