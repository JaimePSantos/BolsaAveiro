from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS,\
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,TT_INTERVALVAR,TT_PROGTEST, TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN,\
    TT_DIFFERENTIALVAR,TT_PROGDIFASSIGN,TT_IN,TT_KEYWORD,TT_IDENTIFIER,TT_IDENTIFIERDIF
from Errors import InvalidSyntaxError
from Nodes import LowerNumberNode,UpperNumberNode,IntervalVarNode,SeparatorNode,BinOpNode,PropOpNode,ProgOpNode,\
    UnaryOpNode,DifferentialVarNode,UnaryProgOpNode,ProgDifNode,UnaryForallOpNode


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

    def parse(self):
        # res = self.intervalExpr()
        res = self.progExpr()
        if not res.error and self.current_tok.type != TT_EOF:
            failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                     "Expected an interval operation."))
            return failure
        return res

    ################################################

    def intervalFactor(self):
        res = ParseResult()
        if self.current_tok.type in TT_FORALL:
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.propEq())
            if res.error: return res
            return res.success(UnaryForallOpNode(tok, factor))
        elif self.current_tok.type in TT_PROGTEST:
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.propExpr())
            if res.error: return res
            if type(factor) is not PropOpNode:
                return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end,
                                                     "Can only perform test action on propositions."))
            return res.success(UnaryProgOpNode(tok, factor))
        elif self.current_tok.type in TT_NOT:
            #TODO: Nao tenho a certeza se este NOT esta correto.
            tok = self.current_tok
            res.register_advancement()
            self.advance()
            factor = res.register(self.propEq())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))
        elif self.current_tok.type in TT_LOWERLIM:
            #TODO: Concatenar isto num so TT_Interval?
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
        elif self.current_tok.type in TT_IDENTIFIER:
            success = res.success(IntervalVarNode(self.current_tok))
            if res.error: return res
            res.register_advancement()
            self.advance()
            return success
        elif self.current_tok.type in TT_IDENTIFIERDIF:
            success = res.success(DifferentialVarNode(self.current_tok))
            if res.error: return res
            res.register_advancement()
            self.advance()
            return success
        elif self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.propExpr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        failure = res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                 "Expected an interval or operator."))
        return failure

    def interval(self):
        return self.bin_op(self.intervalFactor, (TT_SEPARATOR), True)

    def intervalTerm(self):
        return self.bin_op(self.interval,TT_INTERVALMULT)

    def intervalExpr(self):
        return self.bin_op(self.intervalTerm, TT_INTERVALPLUS)

    #TODO: Decidir a prioridade de uma comparacao. Supostamente seria depois da soma, mas acho que nao queremos misturar os 2.
    #TODO: Neste momento podemos somar props logicas com intervalos, nao sei se e suposto permitir isto.
    def propEq(self):
        return self.prop_bin_op(self.intervalExpr,(TT_GT,TT_GEQ,TT_SEQ,TT_ST))

    def propExpr(self):
        # TODO: TT_IN para o forall nao esta muito bom.
        return self.prop_bin_op(self.propEq, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'), (TT_KEYWORD, 'IN')))

    #TODO: Descobrir se podemos fazer um assignment de proposicoes a variaveis.
    def progEq(self):
        return self.prog_bin_op(self.propExpr,(TT_PROGASSIGN,TT_PROGDIFASSIGN))

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
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if res.error: return res
            if Separator:
                left = SeparatorNode(left, op_tok, right)
            else:
                left = BinOpNode(left, op_tok, right)
        return res.success(left)

    def prop_bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            # print(type(left))
            # print(type(right))
            # print(op_tok)
            if res.error: return res
            if op_tok.type in TT_IN:
                if type(left) is not UnaryForallOpNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(left)} is not a for all node.'))
                if type(right) is not PropOpNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
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
            # print(type(left))
            # print(type(right))
            # print(op_tok)
            if op_tok.type in TT_PROGDIFASSIGN:
                if type(left) is not DifferentialVarNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(left)} is not a differential variable.'))
                elif type(right) is not (SeparatorNode and IntervalVarNode):
                    # print(type(right))
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                          f'{str(right)} is not an interval or interval variable.'))
                else:
                    left = ProgDifNode(left,op_tok,right)
                    return res.success(left)
            if op_tok.type in TT_PROGASSIGN:
                if type(left) is not IntervalVarNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(left)} is not an interval variable.'))
                if not(isinstance(right,SeparatorNode) or isinstance(right,IntervalVarNode)):
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(right)} must be an interval or an interval variable.'))
            if op_tok.type in TT_PROGAND:
                if type(right) is not PropOpNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(right)} is not a proposition.'))
                elif type(left) is not ProgDifNode:
                    return res.failure(InvalidSyntaxError(op_tok.pos_start, op_tok.pos_end,
                                                     f'{str(left)} is not a differential equation.'))
            if res.error: return res
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
    if res.error: self.error = res.error
    return res.node

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.last_registered_advance_count == 0:
      self.error = error
    return self

#######################################
# CONTEXT
#######################################

class Context:
  def __init__(self, display_name, parent=None, parent_entry_pos=None):
    self.display_name = display_name
    self.parent = parent
    self.parent_entry_pos = parent_entry_pos
    self.symbol_table = None

#######################################
# SYMBOL TABLE
#######################################

class SymbolTable:
  def __init__(self, parent=None):
    self.symbols = {}
    self.parent = parent

  def get(self, name):
    value = self.symbols.get(name, None)
    if value == None and self.parent:
      return self.parent.get(name)
    return value

  def set(self, name, value):
    self.symbols[name] = value

  def remove(self, name):
    del self.symbols[name]



