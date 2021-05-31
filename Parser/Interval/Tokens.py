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
TT_NEQ = 'NEQ'
TT_GE = 'GE'
TT_NE = 'NE'
TT_NOT = 'NOT'
TT_AND = 'AND'
TT_FORALL = 'FORALL'
TT_BOX = 'BOX'
TT_LOWERLIM = 'LOWERLIM'
TT_UPPERLIM = 'UPPERLIM'
TT_SEPARATOR = 'SEPARATOR'
TT_INTERVALPLUS = 'INTERVALPLUS'
TT_INTERVALMINUS = 'INTERVALMINUS'
TT_INTERVALMULT = 'INTERVALMULT'
TT_INTERVALDIV = 'INTERVALDIV'


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'