import datetime as dt
import time

from core.Lexer import Lexer
from core.Parser import Parser
from core.Translator import Translator


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
    resultString = (
        "\n\n## idDL2dDL v0.1 ################################\n\n"
        "Input in interval dDL:\n\t> " +
        printingInput +
        "\nOutput in dDL:\n\t> " +
        printingResult +
        "\n\n## " +
        dateTime +
        " ##################" +
        "\n## Execution time: " +
        str(
            round(
                executionTime,
                6)) +
        "s ###################\n")
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
