from Parser import Parser, Interpreter
from Lexer import Lexer


def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    # return tokens,error
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    interpreter.visit(ast.node)
    #return ast.node, ast.error

    return None,None