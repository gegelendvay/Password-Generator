import inquirer
import pyperclip
import random
import re
import string

print("Welcome to the Python Password Generator!")

#Check if user input for the password length is an integer or not
try:
    length = int(input("How long would you like your password to be? "))
except ValueError:
    exit("Error: Password length must be a number.")

charSets = {
    "Lowercase": string.ascii_lowercase,
    "Uppercase": string.ascii_uppercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation
}

#Prompt the user to choose from the available charachter types
prompt = [inquirer.Checkbox("options", "Please select the desired charachter types for your password", charSets.keys(), default=["Lowercase"], carousel=True)]

selected = inquirer.prompt(prompt)["options"]
if not selected:
    exit("Error: You must select at least one option.")

generated = []

for i in range(length):
    #For each iteration, randomly select a charachter type from the selected options and add it to a list of generated charachters
    generated.append(random.choice(charSets[random.choice(selected)]))

random.shuffle(generated)
password = "".join(generated)

#Print the generated password, and copy it to the clipboard
print(f'Generated password: {password}')
pyperclip.copy(password)

#Password strength checker function
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