from main import run

while True:
    text = input('basic > ')

    if text == "quit":
        print("Exiting...")
        break

    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())

    else:
        print(result)
