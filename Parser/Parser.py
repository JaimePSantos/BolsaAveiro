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
                                                     "Expected '+', '-', '*' or '/'"))
            return failure
        return res

    ################################################

    def interval(self):
        res = ParseResult()
        tokList = []
        if self.current_tok.type in TT_INTERVALMINUS:
            tokList.append(self.current_tok)
            res.register(self.advance())
            return self.buildInterval(res, tokList)
        elif self.current_tok.type in TT_INTERVALDIV:
            tokList.append(self.current_tok)
            res.register(self.advance())
            return self.buildInterval(res, tokList)
        else:
            return self.buildInterval(res, tokList)

    def intervalExpr(self):
        return self.bin_op(self.interval, (TT_INTERVALPLUS, TT_INTERVALMULT))

    ###################################

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def buildInterval(self, res, tokList):
        if self.current_tok.type in (TT_LOWERLIM, TT_UPPERLIM):
            tokList.append(self.current_tok)
            res.register(self.advance())
            if res.error: return res
            if self.current_tok.type in (TT_INT, TT_FLOAT):
                tokList.append(self.current_tok)
                res.register(self.advance())
                if self.current_tok.type in TT_SEPARATOR:
                    tokList.append(self.current_tok)
                    res.register(self.advance())
                    if self.current_tok.type in (TT_INT, TT_FLOAT):
                        tokList.append(self.current_tok)
                        res.register(self.advance())
                        if self.current_tok.type in (TT_LOWERLIM, TT_UPPERLIM):
                            tokList.append(self.current_tok)
                            res.register(self.advance())
                            return res.success(IntervalNode(tokList))

        failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                 "Expected [ , ] or -"))
        return failure

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


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
