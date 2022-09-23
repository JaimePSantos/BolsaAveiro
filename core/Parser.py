from core.Errors import InvalidSyntaxError
from core.Nodes import (
    LowerNumberNode,
    UpperNumberNode,
    IntervalVarNode,
    SeparatorNode,
    BinOpNode,
    PropOpNode,
    ProgOpNode,
    UnaryOpNode,
    DifferentialVarNode,
    ProgDifNode,
    UnaryForallOpNode,
    BoxPropNode,
    DiamondPropNode,
    NumberNode,
    TestProgNode,
    ParenthesisNode,
    ZeroAryNode,
    CurlyParenthesisNode)
from core.Tokens import (
    TT_INT,
    TT_EOF,
    TT_LOWERLIM,
    TT_UPPERLIM,
    TT_SEPARATOR,
    TT_INTERVALPLUS,
    TT_INTERVALMINUS,
    TT_INTERVALMULT,
    TT_INTERVALDIV,
    TT_GEQ,
    TT_SEQ,
    TT_GT,
    TT_ST,
    TT_NOT,
    TT_FORALL,
    TT_LPAREN,
    TT_RPAREN,
    TT_PROGTEST,
    TT_PROGAND,
    TT_PROGUNION,
    TT_PROGSEQUENCE,
    TT_PROGASSIGN,
    TT_PROGDIFASSIGN,
    TT_IN,
    TT_KEYWORD,
    TT_IDENTIFIER,
    TT_IDENTIFIERDIF,
    TT_LBOX,
    TT_RBOX,
    TT_IMPLIES,
    TT_LDIAMOND,
    TT_RDIAMOND,
    TT_COMMA,
    TT_NDREP,
    TT_LCURLYBRACK,
    TT_RCURLYBRACK,
    TT_FLOAT)


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens) - 1:
            self.next_tok = self.tokens[self.tok_idx + 1]

    def parse(self):
        res = self.progExpr()
        if not res.error and self.current_tok.type != TT_EOF:
            print("Error token: %s" % self.current_tok.type)
            failure = res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected an interval operation."))
            return failure
        return res

    ################################################

    def atom(self):
        res = ParseResult()
        if self.current_tok.type in TT_FORALL:
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.propEq())
            if res.error:
                return res
            return res.success(UnaryForallOpNode(tok, factor))
        elif self.current_tok.type in (TT_INTERVALPLUS, TT_INTERVALMINUS):
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.atom())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        elif self.current_tok.type in TT_LDIAMOND:
            diamond = res.register(
                self.makeWrapperNode(
                    DiamondPropNode,
                    TT_LDIAMOND,
                    TT_RDIAMOND))
            if res.error:
                return res
            success = res.success(diamond)
            return success
        elif self.current_tok.type in TT_LBOX:
            box = res.register(
                self.makeWrapperNode(
                    BoxPropNode, TT_LBOX, TT_RBOX))
            if res.error:
                return res
            success = res.success(box)
            return success
        elif self.current_tok.type in TT_PROGTEST:
            progTest = res.register(
                self.makeWrapperNode(
                    TestProgNode,
                    TT_LPAREN,
                    TT_RPAREN,
                    True))
            if res.error:
                return res
            success = res.success(progTest)
            return success
        elif self.current_tok.type in TT_LPAREN:
            paren = res.register(
                self.makeWrapperNode(
                    ParenthesisNode,
                    TT_LPAREN,
                    TT_RPAREN,
                    False))
            if res.error:
                return res
            success = res.success(paren)
            return success
        elif self.current_tok.type in TT_LCURLYBRACK:
            curl = res.register(
                self.makeWrapperNode(
                    CurlyParenthesisNode,
                    TT_LCURLYBRACK,
                    TT_RCURLYBRACK,
                    False))
            if res.error:
                return res
            success = res.success(curl)
            return success
        elif self.current_tok.type in TT_NOT:
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.propEq())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        elif self.current_tok.type in TT_LOWERLIM:
            # TODO: Concatenar isto num so TT_Interval?
            res.register_advancement()
            self.advance()
            success = res.success(LowerNumberNode(self.current_tok))
            res.register_advancement()
            self.advance()
            return success
        elif self.current_tok.type in TT_INT:
            tokTemp = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type in TT_UPPERLIM:
                success = res.success(UpperNumberNode(tokTemp))
                res.register_advancement()
                self.advance()
                return success
            else:
                success = res.success(NumberNode(tokTemp))
                res.register_advancement()
                # TODO: Por alguma razao a proxima linha tem de estar comentada para o programa funcar.
                # self.advance()
                return success
        elif self.current_tok.type in TT_FLOAT:
            tokTemp = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type in TT_UPPERLIM:
                success = res.success(UpperNumberNode(tokTemp))
                res.register_advancement()
                self.advance()
                return success
            else:
                success = res.success(NumberNode(tokTemp))
                res.register_advancement()
                # TODO: Por alguma razao a proxima linha tem de estar comentada para o programa funcar.
                # self.advance()
                return success
        elif self.current_tok.type in TT_IDENTIFIER:
            success = res.success(IntervalVarNode(self.current_tok))
            if res.error:
                return res
            res.register_advancement()
            self.advance()
            return success
        elif self.current_tok.type in TT_IDENTIFIERDIF:
            success = res.success(DifferentialVarNode(self.current_tok))
            if res.error:
                return res
            res.register_advancement()
            self.advance()
            return success
        failure = res.failure(
            InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected an interval or operator."))
        return failure

    def interval(self):
        return self.bin_op(self.atom, (TT_SEPARATOR), True)

    def intervalTerm(self):
        return self.bin_op(
            self.interval, (TT_INTERVALMULT, TT_INTERVALDIV))

    def intervalExpr(self):
        return self.bin_op(
            self.intervalTerm,
            (TT_INTERVALPLUS,
             TT_INTERVALMINUS))

    def propEq(self):
        return self.prop_bin_op(
            self.intervalExpr, (TT_GT, TT_GEQ, TT_SEQ, TT_ST))

    def propTerm(self):
        # TODO: TT_IN para o forall nao esta muito bom.
        return self.prop_bin_op(
            self.propEq, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'), (TT_KEYWORD, 'IN')))

    def propExpr(self):
        return self.prop_bin_op(self.propTerm, (TT_IMPLIES,))

    def progEq(self):
        return self.prog_bin_op(
            self.propExpr, (TT_PROGASSIGN, TT_PROGDIFASSIGN))

    def progAnd(self):
        return self.prog_bin_op(self.progEq, (TT_PROGAND, TT_COMMA))

    def progExpr(self):
        return self.prog_bin_op(
            self.progAnd, (TT_PROGUNION, TT_PROGSEQUENCE))

    def makeWrapperNode(
            self,
            node,
            firstWrapperToken,
            secondWrapperToken,
            unaryOp=None):
        res = ParseResult()
        element_nodes = []
        boxProp = []
        zeroAryNode = []
        pos_start = self.current_tok.pos_start.copy()
        if unaryOp:
            self.advance()
        if self.current_tok.type != firstWrapperToken:
            return res.failure(InvalidSyntaxError(
                pos_start, self.current_tok.pos_end,
                "Expected '" + str(firstWrapperToken) + "'"
            ))
        res.register_advancement()
        self.advance()
        if self.current_tok.type == secondWrapperToken:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register((self.progExpr())))
            if self.next_tok.type == TT_NDREP:
                self.advance()
                zeroAryNode.append(ZeroAryNode(self.current_tok))
            if res.error:
                return res.failure(
                    InvalidSyntaxError(
                        pos_start,
                        self.current_tok.pos_end,
                        "Expected '{[' , '}]' , 'VAR', '+', '(', 'NOT', '}>' or '<{"))
        if self.current_tok.type != secondWrapperToken and self.current_tok.type != TT_NDREP:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"{str(node)}: Expected ',' or '{str(secondWrapperToken)}' but got {self.current_tok}"
            ))
        elif (self.current_tok.type == secondWrapperToken) and (
                secondWrapperToken == TT_RBOX or secondWrapperToken == TT_RDIAMOND):
            self.advance()
            boxProp.append(res.register((self.progExpr())))
            if self.current_tok.type == TT_RPAREN:
                return res.success(
                    node(
                        element_nodes,
                        boxProp,
                        pos_start,
                        self.current_tok.pos_end.copy()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    pos_start, self.current_tok.pos_end,
                    "Expected a proposition after box program."
                ))
        res.register_advancement()
        self.advance()
        if unaryOp or (unaryOp is not None):
            if (node == ParenthesisNode or node == CurlyParenthesisNode):
                return res.success(
                    node(
                        element_nodes,
                        pos_start,
                        self.current_tok.pos_end.copy(),
                        zeroAryNode))
            else:
                return res.success(
                    node(
                        element_nodes,
                        pos_start,
                        self.current_tok.pos_end.copy()))
        return res.success(
            node(
                element_nodes,
                boxProp,
                pos_start,
                self.current_tok.pos_end.copy()))

    ###################################

    def bin_op(self, func, ops, Separator=None):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            # print(type(right))
            if res.error:
                return res
            if Separator:
                if not (isinstance(right, UpperNumberNode)):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected a number followed by a ']'."))
                left = SeparatorNode(left, op_tok, right)
            else:
                left = BinOpNode(left, op_tok, right)
        return res.success(left)

    def prop_bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops or (
                self.current_tok.type,
                self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if res.error:
                return res
            if op_tok.type in TT_IN:
                if not isinstance(left, UnaryForallOpNode):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(left)} is not a for all node.'))
                if not isinstance(right, PropOpNode):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(right)} is not a proposition.'))
            left = PropOpNode(left, op_tok, right)
        return res.success(left)

    def prog_bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if op_tok.type in TT_PROGDIFASSIGN:
                if not isinstance(left, DifferentialVarNode):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(left)} is not a differential variable.'))
                elif not (isinstance(right, SeparatorNode) or isinstance(right, IntervalVarNode) or isinstance(right,
                                                                                                               UnaryOpNode) or isinstance(
                        right, BinOpNode) or isinstance(right, NumberNode)):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(right)} is not an interval or interval variable.'))
                else:
                    left = ProgDifNode(left, op_tok, right)
                    return res.success(left)

            if op_tok.type in TT_PROGASSIGN:
                if not isinstance(left, IntervalVarNode):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(left)} is not an interval variable.'))
                if not (
                    isinstance(
                        right,
                        SeparatorNode) or isinstance(
                        right,
                        IntervalVarNode) or isinstance(
                        right,
                        ParenthesisNode) or isinstance(
                        right,
                        BinOpNode)):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(right)} must be an interval or an interval variable.'))
            if op_tok.type in TT_PROGAND:
                # TODO: Se tiver uma coisa que nao e uma prop dentro de
                # um parentises isto deixa fazer o progAnd.
                if not (
                    isinstance(
                        right,
                        PropOpNode) or isinstance(
                        right,
                        ParenthesisNode)):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(right)} is not a proposition.'))
                # TODO: ProgOpNode agora pode ser uma equacao
                # diferencial. Esta restricao nao e suficiente.
                elif not (isinstance(left, ProgDifNode) or isinstance(left, ProgOpNode)):
                    return res.failure(
                        InvalidSyntaxError(
                            op_tok.pos_start,
                            op_tok.pos_end,
                            f'{str(left)} is not a differential equation.'))
            if res.error:
                return res
            left = ProgOpNode(left, op_tok, right)
        return res.success(left)


#######################################
# PARSE RESULT
#######################################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self
