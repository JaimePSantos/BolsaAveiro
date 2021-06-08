from main import run

while True:

    fileOpen = input('Do you want to read a file? y/n')
    resultList = []
    errorList = []
    if fileOpen.lower() == 'Y'.lower():
        file = input('Enter file name.')
        with open(f'{file}.txt') as f:
            text = f.readlines()
            # print(text)
        for line in text:
            # print(line)
            result, error = run(file, line)
            if error:
                errorList.append(error)
            resultList.append(result)
    else:
        text = input('Intervals > ')
        if text == "q":
            print("Exiting...")
            break
        result, error = run('<stdin>', text)

    if errorList:
        for er in errorList:
            print(er.as_string())
    elif error:
        print(er.as_string())

    else:
        if not resultList:
            print(result)
        else:
            for res in resultList:
                print(res)

