import pathlib as pl

from iddl.RunProgram import run, run2, run3,runTranslatorTest,runInterpTest

def runFile(filename):
    resultList = []
    filePath = str(pl.Path().resolve()) + \
        '\\InputFiles' + '\\' + filename + '.txt'
    resultFile = pl.Path(filePath)
    if not (resultFile):
        return False
    with open(filePath) as f:
        text = f.readlines()
        for line in text:
            if '#' in line:
                continue
            if line == '\n':
                continue
            result, error = run2(filename, line)
            if error:
                print(error.as_string())
                break
            else:
                resultList.append(result)
    return resultList


def writeFile(fileName, filePath, result, multipleLines, writeMethod):
    with open(filePath, writeMethod) as f:
        f.write("Theorem \" " + fileName + ' \"\n\nProblem\n\n')
        if multipleLines:
            for line in result:
                f.write(line + '\n')
        else:
            f.write(result + '\n')
        f.write("\nEnd.")
        f.write("\nEnd.")


def printToFile(result, multipleLines):
    fileName = input('\tFile name? > ')
    fileNameKX = fileName + '.kyx'
    filePath = str(pl.Path().resolve()) + \
        '\\OutputFiles' + '\\' + fileNameKX
    resultFile = pl.Path(filePath)
    if resultFile.is_file():
        rewrite = input(
            '\t' +
            fileName +
            ' already exists. Rewrite file? y/n > ').lower()
        if rewrite:
            writeFile(fileName, filePath, result, multipleLines, 'w')
            print("File at %s successfully rewritten.\n" % filePath)
            return filePath
        else:
            printToFile(result)
    else:
        writeFile(fileName, filePath, result, multipleLines, 'a')
        print("File at %s successfully created.\n" % filePath)
    return filePath


def availableCommands():
    availableCmds = (
        'Commands:' +
        '\n    -> help: lists available commands.' +
        '\n    -> q: exits the program.' +
        '\n    -> run: prompts for a file of formulas to be translated.\n')
    return availableCmds


def main():
    resultList = []
    print('Starting idDL2dDL... \nType "help" for available commands.')
    while True:
        text = input('Intervals > ')
        text = text.strip()
        if text == "q":
            print("Exiting...")
            break
        elif text.lower() == 'help'.lower():
            print(availableCommands())
            continue
        elif text.lower() == 'run'.lower():
            fn = input('Enter file name: ')
            fn = fn.strip()
            result = runFile(fn)
            if not result:
                continue
            toFile = input('Generate file with results? y/n > ').lower()
            if toFile == 'y'.lower():
                printToFile(result, True)
                continue
            else:
                continue
        result, error = run2('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            toFile = input('Generate file with results? y/n > ').lower()
            if toFile == 'y'.lower():
                printToFile(result, False)
                continue
            else:
                continue

main()
