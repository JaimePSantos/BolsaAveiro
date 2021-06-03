from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,TT_INTERVALVAR,TT_PROGTEST, TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN
from Errors import InvalidSyntaxError
from Nodes import PrettyLowerNumberNode,PrettyUpperNumberNode,PrettyIntervalVarNode,PrettySeparatorNode,\
    PrettyBinOpNode,PrettyPropOpNode,PrettyProgOpNode,PrettyUnaryOpNode

#######################################
# PARSER
#######################################

class PrettyParser:
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
        # res = self.intervalExpr()
        # res = self.propExpr()
        res = self.progExpr()
        if not res.error and self.current_tok.type != TT_EOF:
            failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                     "Expected an interval operation."))
            return failure
        return res

    ################################################

    def intervalFactor(self):
        res = ParseResult()
        if self.current_tok.type in TT_PROGTEST:
            tok = self.current_tok
            res.register(self.advance())
            factor = res.register(self.propExpr())
            if res.error: return res
            return res.success(PrettyUnaryOpNode(tok, factor))
        if self.current_tok.type in TT_NOT:
            #TODO: Nao tenho a certeza se este NOT esta correto.
            tok = self.current_tok
            res.register(self.advance())
            factor = res.register(self.intervalEq())
            if res.error: return res
            return res.success(PrettyUnaryOpNode(tok, factor))

        elif self.current_tok.type in TT_LOWERLIM:
            res.register(self.advance())
            success = res.success(PrettyLowerNumberNode(self.current_tok))
            res.register(self.advance())
            return success

        elif self.current_tok.type in TT_INT:
            tokTemp = self.current_tok
            res.register(self.advance())
            if self.current_tok.type in TT_UPPERLIM:
                success = res.success(PrettyUpperNumberNode(tokTemp))
                res.register(self.advance())
                return success

        elif self.current_tok.type in TT_INTERVALVAR:
            success = res.success(PrettyIntervalVarNode(self.current_tok))
            res.register(self.advance())
            return success

        elif self.current_tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.propExpr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                 "Expected an interval or interval operation ( - or /)."))
        return failure

    def interval(self):
        return self.bin_op(self.intervalFactor, TT_SEPARATOR, True)

    def intervalTerm(self):
        return self.bin_op(self.interval,TT_INTERVALMULT)

    def intervalExpr(self):
        return self.bin_op(self.intervalTerm, TT_INTERVALPLUS)

    #TODO: Decidir a prioridade de uma igualdade. Deve ser depois da soma mas antes do &?
    #TODO: Neste momento podemos somar props logicas com intervalos, nao sei se e suposto permitir isto.
    def propEq(self):
        return self.bin_op(self.intervalExpr,(TT_GT,TT_GEQ,TT_SEQ,TT_ST))

    def propExpr(self):
        return self.prop_bin_op(self.propEq, (TT_AND))

    def progEq(self):
        #TODO: Descobrir se o termo é uma proposiçao ou apenas intervalo.
        return self.prog_bin_op(self.propExpr,TT_PROGASSIGN)

    def progAnd(self):
        return self.prog_bin_op(self.progEq,(TT_PROGAND))
    def progExpr(self):
        return self.prog_bin_op(self.progAnd,(TT_PROGUNION,TT_PROGSEQUENCE))
    ###################################

    def bin_op(self, func, ops, Separator=None):
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
                left = PrettySeparatorNode(left, op_tok, right)
            else:
                left = PrettyBinOpNode(left, op_tok, right)
        return res.success(left)

    def prop_bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = PrettyPropOpNode(left, op_tok, right)
        return res.success(left)

    def prog_bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = PrettyProgOpNode(left, op_tok, right)
        return res.success(left)

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
