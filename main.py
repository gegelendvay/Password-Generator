import inquirer
import pyperclip
import random
import re
import string

print("Welcome to the Python Password Generator!")
try:
    length = int(input("How long would you like your password to be? "))
except ValueError:
    exit("Error: Password length must be a number.")

prompt = [
    inquirer.Checkbox("options", "Please select the desired charachter types for your password", ["Lowercase", "Uppercase", "Numbers", "Symbols"], default=["Lowercase"], carousel=True)
]

options = inquirer.prompt(prompt)["options"]
if not options:
    exit("Error: You must select at least one option.")

generated = []

for i in range(length):
    current = random.choice(options)
    if "Lowercase" in current:
        generated.append(random.choice(string.ascii_lowercase))
    elif "Uppercase" in current:
        generated.append(random.choice(string.ascii_uppercase))
    elif "Numbers" in current:
        generated.append(random.choice(string.digits))
    elif "Symbols" in current:
        generated.append(random.choice(string.punctuation))

random.shuffle(generated)
password = "".join(generated)
print(f'Generated password: {password}')
pyperclip.copy(password)

#Password strength
def passwordStrength(password):
    if len(password) <= 8:
        return "Weak"
    if re.search(r"\d|[A-Z]", password) and re.search(r"[\W_]", password):
        return "Strong"
    return "Medium"

print(f'Password strength: {passwordStrength(password)}')