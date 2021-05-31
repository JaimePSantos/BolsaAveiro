from Tokens import Token, TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX
from Errors import IllegalCharError


DIGITS = '0123456789'


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.next_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        self.next_char = self.text[self.pos.idx+1] if self.pos.idx < len(self.text)-1 else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '[':
                tokens.append(Token(TT_LOWERLIM, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_UPPERLIM, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_SEPARATOR, pos_start=self.pos))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_INTERVALPLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_INTERVALMINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_INTERVALMULT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_INTERVALDIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '>':
                if self.next_char == '=':
                    tokens.append(Token(TT_GEQ, pos_start=self.pos))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TT_GT, pos_start=self.pos))
                    self.advance()
            elif self.current_char == '<':
                if self.next_char == '=':
                    tokens.append(Token(TT_SEQ, pos_start=self.pos))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TT_ST, pos_start=self.pos))
                    self.advance()
            elif self.current_char == '!':
                tokens.append(Token(TT_NOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '&':
                tokens.append(Token(TT_AND, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)