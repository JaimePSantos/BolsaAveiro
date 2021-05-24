from main import run

while True:
    text = input('basic > ')
    result, error = run('<stdin>', text)

    if text == "quit": 
        print("Exiting...") 
        break

    if error:
        print(error.as_string())

    else:
        print(result)
