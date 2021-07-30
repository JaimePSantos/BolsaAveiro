from main import run
import pathlib as pl
import os.path
def runFile(filename):
    resultList = []
    filePath = str(pl.Path().resolve()) + '\\InputFiles' + '\\' + filename +'.txt'
    resultFile = pl.Path(filePath)
    if not(resultFile):
        return False
    with open(filePath) as f:
        text = f.readlines()
        for line in text:
            if '#' in line:
                continue
            if line == '\n':
                continue
            result, error = run(filename, line)
            if error:
                print(error.as_string())
                break
            else:
                resultList.append(result)
    return resultList

def printToFile(result,multipleLines):
    fileName = input('\tFile name? > ')
    fileNameKX = fileName + '.kyx'
    filePath = str(pl.Path().resolve())+'\\OutputFiles' +'\\'+ fileNameKX
    resultFile = pl.Path(filePath)
    if resultFile.is_file():
        rewrite = input('\t'+fileName+' already exists. Rewrite file? y/n > ').lower()
        if rewrite:
            with open(filePath, 'w') as f:
                f.write("Theorem \" "+fileName + ' \"\n\nProblem\n\n')
                if multipleLines:
                    for line in result:
                        f.write(line + '\n')
                else:
                    f.write(result+'\n')
                f.write("\nEnd.")
                f.write("\nEnd.")
            return filePath
        else:
            printToFile(result)
    with open(filePath,'a') as f:
        f.write("Theorem \" " + fileName + '\"\n\nProblem\n\n')
        if multipleLines:
            for line in result:
                f.write(line + '\n')
        else:
            f.write(result + '\n')
        f.write("\nEnd.")
        f.write("\nEnd.")
    return filePath


def main():
    resultList = []
    while True:
        text = input('Intervals > ')
        text = text.strip()
        if text == "q":
            print("Exiting...")
            break
        elif text.lower() == 'run'.lower():
            fn = input('Enter file name: ')
            fn = fn.strip()
            result = runFile(fn)
            if not result:
                continue
            toFile = input('Generate file with results? y/n > ').lower()
            if toFile == 'y'.lower():
                printToFile(result,True)
                continue
            else:
                continue
        result, error = run('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            print(result)
        toFile = input('Generate file with results? y/n > ').lower()
        if toFile == 'y'.lower():
            printToFile(result,False)
            continue
        else:
            continue
main()