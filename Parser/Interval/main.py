from Lexer import Lexer
from Interpreter import Interpreter
from Parser import Parser
from PrettyParser import PrettyParser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    print("\nLEXER: %s\n"%tokens)
    #
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    print("PARSER: %s\n"%ast.node)

    prettyParser = PrettyParser(tokens)
    prettyAst = prettyParser.parse()
    if ast.error:
        return None, ast.error
    print("PRETTYPARSER: %s\n"%prettyAst.node)

    # interpreter = Interpreter()
    # interpreter.reset()
    # result = interpreter.visit(ast.node)
    # print("INTERPRETER: %s\n"%result)

    return 1,None