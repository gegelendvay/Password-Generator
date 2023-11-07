import inquirer
import pyperclip
import secrets
import string

print("Welcome to the Python Password Generator!")

# Improved input handling
while True:
    try:
        length = int(input("How long would you like your password to be? "))
        if length <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Error: Password length must be a number.")

char_sets = {
    "Lowercase": string.ascii_lowercase,
    "Uppercase": string.ascii_uppercase,
    "Numbers": string.digits,
    "Symbols": string.punctuation
}

prompt = [
    inquirer.Checkbox("options",
                      message="Please select the desired character types for your password",
                      choices=list(char_sets.keys()),
                      default=["Lowercase"],
                      carousel=True)
]

selected_types = inquirer.prompt(prompt)["options"]
if not selected_types:
    exit("Error: You must select at least one option.")

# Ensure at least one character from each selected set is included
selected_chars = "".join([secrets.choice(char_sets[type]) for type in selected_types])
required_length = max(length, len(selected_types))
remaining_chars = "".join([char_sets[type] for type in selected_types])

generated = [secrets.choice(remaining_chars) for _ in range(required_length - len(selected_types))]
generated.extend(selected_chars)
secrets.SystemRandom().shuffle(generated)
password = "".join(generated)

print(f'Generated password: {password}')
try:
    pyperclip.copy(password)
    print('The password has been copied to your clipboard.')
except pyperclip.PyperclipException:
    print('Could not copy the password to your clipboard. Please copy it manually.')

# Improved password strength checker function
def password_strength(password):
    length = len(password)
    if length < 8:
        return "Weak"
    if (re.search(r"\d", password) and re.search(r"[A-Z]", password) and
        re.search(r"[\W_]", password) and length >= 12):
        return "Strong"
    return "Medium"

print(f'Password strength: {password_strength(password)}')
