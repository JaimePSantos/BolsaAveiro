from main import run

def runFile(filename):
    try:
        with open(f'{filename}.txt') as f:
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
                    print(result)
    except Exception as e:
        print(e)

def main():
    while True:
        text = input('Intervals > ')
        if text == "q":
            print("Exiting...")
            break
        elif text == 'run':
            fn = input('Enter file name: ')
            runFile(fn)
            continue
        result, error = run('<stdin>', text)
        if error:
            print(error.as_string())

        else:
            print(result)
main()