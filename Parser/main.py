from Lexer import Lexer
from Interpreter import Interpreter
from Parser import Parser


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
    interpreter.reset()
    result = interpreter.visit(ast.node)
    # print(interpreter.upperNumberList)
    # print(interpreter.lowerNumberList)
    #return ast.node, ast.error

    return result,None