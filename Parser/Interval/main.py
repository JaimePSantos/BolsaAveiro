from Lexer import Lexer
from Translator import Translator
from Interpreter import Interpreter
from Parser import Parser
from PrettyParser import PrettyParser
import datetime as dt
import time
import textwrap as tw

def run(fn, text):
    start_time = time.time()
    lexer = Lexer(fn, text)
    tokens, error = lexer.makeTokens()
    if error:
        return None, error
    # print("\nLEXER:\t %s\n"%tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    # print("PARSER:\t %s\n"%ast.node)

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast.node)
    result = translator.buildTranslation()
    # wrapper = tw.TextWrapper()
    # wrapper.subsequent_indent= "\t\t"
    # printingResult = wrapper.fill(result)
    printingResult = result.split()
    for i in range(len(printingResult)-1):
        if(printingResult[i+1]=='++' or printingResult[i+1]=='->'):
            printingResult[i]+='\n\t\t'
    printingResult = ' '.join(printingResult)
    dateTime = str(dt.datetime.now())
    print("")
    print("")
    print("## idDL2dDL v0.1 ################################")
    print("")
    print("Input in interval dDL:\n\t> %s"%text)
    print("Output in dDL:\n\t> %s"%printingResult)
    print("")
    executionTime = time.time() - start_time
    print("## "+dateTime+" ##################")
    print("## Execution time: %s s"%round(executionTime,6) +" ##################")

    # prettyParser = PrettyParser(tokens)
    # prettyAst = prettyParser.parse()
    # if ast.error:
    #     return None, ast.error
    # print("PRETTYPARSER: %s\n"%prettyAst.node)

    # interpreter = Interpreter()
    # interpreter.reset()
    # result = interpreter.visit(ast.node)
    # print("INTERPRETER: %s\n"%result)

    return "",None