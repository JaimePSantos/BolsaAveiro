from Lexer import Lexer
from Translator import Translator
from Interpreter import Interpreter
from Parser import Parser
from PrettyParser import PrettyParser
import datetime as dt
import time
import textwrap as tw

def prettyPrint(text,linebreak):
    printingResult = text.split()
    for i in range(len(printingResult)-1):
        if(printingResult[i+1] in linebreak):
            printingResult[i]+='\n\t\t'
    printingResult = ' '.join(printingResult)
    return printingResult

def resultsString(input,output,time):
    printingInput =  prettyPrint(input,['||','->'])
    printingResult = prettyPrint(output,['++','->'])
    dateTime = str(dt.datetime.now())
    executionTime = time
    resultString = ("\n\n## idDL2dDL v0.1 ################################\n\n"
                    "Input in interval dDL:\n\t> " + printingInput +
                    "\nOutput in dDL:\n\t> " + printingResult +
                    "\n\n## " + dateTime + " ##################" +
                    "\n## Execution time: %s s"%round(executionTime,6) +" ##################\n")

    return resultString

def run(fn, input):
    start_time = time.time()
    lexer = Lexer(fn, input)
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
    output = translator.buildTranslation()
    executionTime = time.time() - start_time
    printingResults = resultsString(input,output,executionTime)
    print(printingResults)

    # interpreter = Interpreter()
    # interpreter.reset()
    # result = interpreter.visit(ast.node)
    # print("INTERPRETER: %s\n"%result)

    return output,None