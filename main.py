import inquirer
import pyperclip
import re
import secrets
import string
import termios

print("Welcome to the Python Password Generator!")

# Check if user input for the password length is an integer or not if not, retry until the user enters a valid input
while True:
    try:
        length = int(input("How long would you like your password to be? "))
        if length < 1:
            print("You must enter a number greater than 0.")
            continue
        break
    except ValueError:
        print("Error: Password length must be a number.")

charSets = {
    "Lowercase": string.ascii_lowercase,
    "Uppercase": string.ascii_uppercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation
}

# Prompt the user to choose from the available character types
prompt = [inquirer.Checkbox("options", "Please use the arrow keys and space bar to select the desired character types for your password", charSets.keys(), default=["Lowercase"], carousel=True)]

while True:
    try:
        selected = inquirer.prompt(prompt)["options"]
    except termios.error:
        exit("A Prompt Error Occurred, are you running this script in a terminal? (inquirer does not work in IDEs)")
    if selected:
        break
    print("You must select at least one option.")

chars = "".join([secrets.choice(charSets[i]) for i in selected])
remaining = "".join([charSets[i] for i in selected])
additional = [secrets.choice(remaining) for _ in range(length - len(selected))]

generated = list(chars + "".join(additional))
secrets.SystemRandom().shuffle(generated)
password = "".join(generated)

# Print the generated password, and copy it to the clipboard
print(f'Generated password: {password}')
try:
    pyperclip.copy(password)
except pyperclip.PyperclipException:
    print('Could not automatically copy the password to your clipboard, please copy it manually.')

# Password strength checker function
def passwordStrength(password):
    """
    Determines the strength of the password

    Args:
        password (str): The password to be checked

    Returns:
        str: 'Weak' for passwords with less than 9 chars

            'Strong' for passwords that contain a number and/or a capital letter and a symbol

            'Medium' for every other password
    """
    if len(password) <= 8:
        return "Weak"
    if re.search(r"\d|[A-Z]", password) and re.search(r"[\W_]", password):
        return "Strong"
    return "Medium"

print(f'Password strength: {passwordStrength(password)}')