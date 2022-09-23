TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF = 'EOF'
TT_GEQ = 'GEQ'
TT_SEQ = 'SEQ'
TT_GT = 'GT'
TT_ST = 'ST'
TT_NOT = 'NOT'
TT_AND = 'AND'
TT_FORALL = 'FORALL'
TT_IN = 'IN'
TT_BOX = 'BOX'
TT_LOWERLIM = 'LOWERLIM'
TT_UPPERLIM = 'UPPERLIM'
TT_SEPARATOR = 'SEPARATOR'
TT_INTERVALPLUS = 'INTERVALPLUS'
TT_INTERVALMINUS = 'INTERVALMINUS'
TT_INTERVALMULT = 'INTERVALMULT'
TT_INTERVALDIV = 'INTERVALDIV'
TT_INTERVALVAR = 'INTERVALVAR'
TT_PROGTEST = 'PROGRAMTEST'
TT_PROGAND = 'PROGAND'
TT_PROGUNION = 'PROGUNION'
TT_PROGSEQUENCE = 'PROGSEQUENCE'
TT_PROGASSIGN = 'PROGASSIGN'
TT_PROGDIFASSIGN = 'PROGDIFASSIGN'
TT_DIFFERENTIALVAR = 'DIFFERENTIALVAR'
TT_KEYWORD = 'KEYWORD'
TT_IDENTIFIER = 'IDENTIFIER'
TT_IDENTIFIERDIF = 'IDENTIFIERDIF'
TT_LBOX = 'LBOX'
TT_RBOX = 'RBOX'
TT_LDIAMOND = 'LDIAMOND'
TT_RDIAMOND = 'RDIAMOND'
TT_IMPLIES = 'IMPLIES'
TT_DEBUG = 'DEBUG'
TT_COMMA = 'COMMA'
TT_NDREP = 'NDREP'
TT_RCURLYBRACK = 'RCURLYBRACK'
TT_LCURLYBRACK = 'LCURLYBRACK'


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    def __add__(self,other):
        value = eval(str(self.value)+str(other.value))
        type = self.type + "_" + other.type
        return Token(type, value,self.pos_start,self.pos_end)
