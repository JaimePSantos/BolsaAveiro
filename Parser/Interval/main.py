from Lexer import Lexer
from Translator import Translator
from Interpreter import Interpreter
from Parser import Parser, SymbolTable
from PrettyParser import PrettyParser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()
    if error:
        return None, error
    print("\nLEXER:\t %s\n"%tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    print("PARSER:\t %s\n"%ast.node)

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast.node)
    result = translator.buildTranslation()
    print("Translator: %s\n"%result)
    print("####################################################################################\n")

    # prettyParser = PrettyParser(tokens)
    # prettyAst = prettyParser.parse()
    # if ast.error:
    #     return None, ast.error
    # print("PRETTYPARSER: %s\n"%prettyAst.node)

    # interpreter = Interpreter()
    # interpreter.reset()
    # result = interpreter.visit(ast.node)
    # print("INTERPRETER: %s\n"%result)

    return 1,None