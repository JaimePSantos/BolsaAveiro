from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV
from Errors import InvalidSyntaxError
from Nodes import IntervalNode, BinOpNode
from ParseResult import ParseResult


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
        else:
            return self.buildInterval(res, tokList)

    def intervalExpr(self):
        return self.bin_op(self.interval, (TT_INTERVALPLUS, TT_INTERVALDIV, TT_INTERVALMULT))

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
