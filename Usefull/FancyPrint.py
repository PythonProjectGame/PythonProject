import time


def Print(text: str, root: object, label: object) -> None:
    output = ""

    for i in text:
        if i == chr(32):
            output += " "
            continue

        if i == "/":
            output += "\n"
            continue

        for j in range(65, 123):
            bruteLetter = chr(j)
            time.sleep(0.005)

            label.config(text=output + bruteLetter)
            root.update()

            if bruteLetter == i:
                output += bruteLetter
                break