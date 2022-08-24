import datetime as dt
import time

from core.Lexer import Lexer
from core.Parser import Parser
from core.Translator import Translator
from core.Interpreter import Interpreter


def prettyPrint(text, linebreak):
    printingResult = text.split()
    for i in range(len(printingResult) - 1):
        if (printingResult[i + 1] in linebreak):
            printingResult[i] += '\n\t\t'
    printingResult = ' '.join(printingResult)
    return printingResult


def resultsString(input, output, time):
    printingInput = prettyPrint(input, ['||', '->'])
    printingResult = prettyPrint(output, ['++', '->'])
    dateTime = str(dt.datetime.now())
    executionTime = time
    resultString = ("\n\n## idDL2dDL v0.1 ################################\n\n"
                    "Input in interval dDL:\n\t> " + printingInput +
                    "\nOutput in dDL:\n\t> " + printingResult +
                    "\n\n## " + dateTime + " ##################" +
                    "\n## Execution time: " + str(round(executionTime, 6)) + "s ###################\n")
    return resultString


def run(fn, input):
    start_time = time.time()
    lexer = Lexer(fn, input)
    tokens, error = lexer.makeTokens()
    print(f"First tokens->{tokens}")
    if error:
        return None, error
    # print("\nLEXER:\t %s\n"%tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return ast.error
    # print("PARSER:\t %s\n"%ast.node)

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast.node)
    output = translator.buildTranslation()
    executionTime = time.time() - start_time
    printingResults = resultsString(input, output, executionTime)
    print(printingResults)

    return output, None


def runGUI(fn, input):
    lexer = Lexer(fn, input)
    tokens, error = lexer.makeTokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast.node)
    output = translator.buildTranslation()

    return output

def runInterpGUI(fn, input):
    print(f"Input: {input}")
    lexer = Lexer(fn, input)
    tokens, error = lexer.makeTokens()
    print(f"First tokens->{tokens}")
    if error:
        print(error)
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        print(ast.error)
        return ast.error

    interp = Interpreter()
    visitInterp = interp.visit(ast.node)
    outInterp = interp.getTranslation()

    lexer2 = Lexer(fn, outInterp)
    tokens2, error2 = lexer2.makeTokens()
    if error2:
        return None,error2

    parser2 = Parser(tokens2)
    ast2 = parser2.parse()
    if ast2.error:
        return ast2.error

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast2.node)
    output = translator.buildTranslation()
    return output

def run2(fn, input):
    start_time = time.time()
    print(f"Input: {input}")
    lexer = Lexer(fn, input)
    tokens, error = lexer.makeTokens()
    print(f"First tokens->{tokens}")
    if error:
        print(error)
        return None, error
    # print("\nLEXER:\t %s\n"%tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    # print(type(ast.node))
    # print(ast.node)
    if ast.error:
        print(ast.error)
        return ast.error
    # print("PARSER:\t %s\n"%ast.node)

    interp = Interpreter()
    visitInterp = interp.visit(ast.node)
    outInterp = interp.getTranslation()
    # print(f"outinterp : {outInterp}")

    lexer2 = Lexer(fn, outInterp)
    tokens2, error2 = lexer2.makeTokens()
    # print(f"Second tokens->{tokens2}")
    if error2:
        print(error2)
        return None,error2
    # print("\nLEXER:\t %s\n"%tokens)

    parser2 = Parser(tokens2)
    ast2 = parser2.parse()
    if ast2.error:
        print(ast2.error)
        return ast2.error
    # print("PARSER:\t %s\n"%ast.node)

    translator = Translator()
    translator.reset()
    visitNodes = translator.visit(ast2.node)
    output = translator.buildTranslation()
    executionTime = time.time() - start_time
    printingResults = resultsString(input, output, executionTime)
    print(printingResults)

    return output, None

def run3(fn, input):
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
    # print(str(ast.node))
    # translator = Translator()
    # translator.reset()
    # visitNodes = translator.visit(ast.node)
    # output = translator.buildTranslation()
    output = str(Interpreter().visit(ast.node))
    executionTime = time.time() - start_time
    printingResults = resultsString(input, output, executionTime)
    # print(printingResults)
    print(f"Interpreted Result -> {output}")
    return output, None