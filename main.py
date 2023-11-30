import inquirer
import pyperclip
import re
import secrets
import string
import termios

MIN_PASSWORD_LENGTH = 8


def get_password_length():
    while True:
        try:
            length = int(input("How long would you like your password to be? "))
            if length < 1:
                print("You must enter a number greater than 0.")
                continue
            return length
        except ValueError:
            print("Error: Password length must be a number.")


def get_selected_options(charSets):
    prompt = [
        inquirer.Checkbox(
            "options",
            "Please use the arrow keys and space bar to select the desired character types for your password",
            charSets.keys(),
            default=["Lowercase"],
            carousel=True,
        )
    ]

    while True:
        try:
            selected = inquirer.prompt(prompt)["options"]
        except termios.error:
            exit(
                "A Prompt Error Occurred, are you running this script in a terminal? (inquirer does not work in IDEs)"
            )

        if selected:
            return selected

        print("You must select at least one option.")


def generate_password(selected, length, charSets):
    chars = "".join([secrets.choice(charSets[i]) for i in selected])
    remaining = "".join([charSets[i] for i in selected])
    additional = [secrets.choice(remaining) for _ in range(length - len(selected))]

    generated = list(chars + "".join(additional))
    secrets.SystemRandom().shuffle(generated)
    password = "".join(generated)

    return password


def password_strength(password):
    if len(password) <= MIN_PASSWORD_LENGTH:
        return "Weak"
    if re.search(r"\d|[A-Z]", password) and re.search(r"[\W_]", password):
        return "Strong"
    return "Medium"


def main():
    print("Welcome to the Python Password Generator!")

    length = get_password_length()

    charSets = {
        "Lowercase": string.ascii_lowercase,
        "Uppercase": string.ascii_uppercase,
        "Numbers": string.digits,
        "Symbols": string.punctuation,
    }

    selected = get_selected_options(charSets)

    password = generate_password(selected, length, charSets)

    print(f"Generated password: {password}")

    try:
        pyperclip.copy(password)
    except pyperclip.PyperclipException as e:
        print(
            f"Could not copy the password to the clipboard: {e}. Please copy it manually."
        )

    print(f"Password strength: {password_strength(password)}")


if __name__ == "__main__":
    main()
