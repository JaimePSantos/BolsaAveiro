from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,Token,TT_INTERVALVAR,TT_PROGTEST,TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN,\
    TT_DIFFERENTIALVAR,TT_PROGDIFASSIGN,TT_IN,TT_KEYWORD,TT_IDENTIFIER
from Errors import IllegalCharError
import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters + "'"
LETTERS_DIGITS = LETTERS + DIGITS
KEYWORDS = [
	'VAR',
	'AND',
	'OR',
	'NOT'
]

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.next_char = None
        self.prev_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        self.next_char = self.text[self.pos.idx+1] if self.pos.idx < len(self.text)-1 else None
        self.prev_char = self.text[self.pos.idx-1] if (self.pos.idx < len(self.text)+1 and len(self.text) > 0) else None

    #TODO: Tem que haver melhor maneira de fazer tokens.
    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_letter())
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
            # elif self.current_char == '/':
            #     tokens.append(Token(TT_INTERVALDIV, pos_start=self.pos))
            #     self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '!':
                tokens.append(Token(TT_NOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '&':
                if self.next_char == '&':
                    tokens.append(Token(TT_PROGAND,pos_start=self.pos))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TT_AND, pos_start=self.pos))
                    self.advance()
            elif self.current_char == '|':
                if self.next_char == '|':
                    tokens.append(Token(TT_PROGUNION,pos_start=self.pos))
                    self.advance()
                    self.advance()
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            elif self.current_char == '?':
                tokens.append(Token(TT_PROGTEST, pos_start=self.pos))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_PROGSEQUENCE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=' :
                if self.prev_char != ':':
                    tokens.append(Token(TT_PROGDIFASSIGN, pos_start=self.pos))
                    self.advance()
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            elif self.current_char == ':':
                if self.next_char == '=':
                    tokens.append(Token(TT_PROGASSIGN,pos_start=self.pos))
                    self.advance()
                    self.advance()
                else:
                    pos_start = self.pos.copy()
                    char = self.current_char
                    self.advance()
                    return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
            elif self.current_char == '$':
                tokens.append(Token(TT_FORALL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_IN, pos_start=self.pos))
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

    def make_letter(self):
        post_start = self.pos.copy()
        letter_str = ''
        while self.current_char is not None and self.current_char in LETTERS:
            letter_str+=self.current_char
            self.advance()
        if "'" in letter_str:
            return Token(TT_DIFFERENTIALVAR,str(letter_str), post_start, self.pos)
        return Token(TT_INTERVALVAR, str(letter_str), post_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
    # def make_not_equals(self):
    #     pos_start = self.pos.copy()
    #     self.advance()
    #
    #     if self.current_char == '=':
    #         self.advance()
    #         return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
    #
    #     self.advance()
    #     return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    # def makeEquals(self):
    #     tok_type = TT_EQ
    #     pos_start = self.pos.copy()
    #     self.advance()
    #
    #     if self.current_char == '=':
    #         self.advance()
    #         tok_type = TT_EE
    #
    #     return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_ST
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_SEQ

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GEQ

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

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