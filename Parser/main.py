from Parser import Parser
from Lexer import Lexer


def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # if error: return None, error
    # return tokens,error
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
