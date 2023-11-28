import tkinter as tk
from tkinter import messagebox
import pyperclip
import random
import re
import string

def generate_password():
    charSets = {
        "Lowercase": string.ascii_lowercase,
        "Uppercase": string.ascii_uppercase,
        "Numbers": string.digits,
        "Symbols": string.punctuation
    }

    # Get the selected character types
    selected = [checkbox_vars[char_type].get() for char_type in charSets.keys()]

    if not any(selected):
        messagebox.showerror("Error", "You must select at least one option.")
        return

    # Validate password length
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Password length must be a number.")
        return

    generated = []

    for _ in range(length):
        # For each iteration, randomly select a character type from the selected options
        # and add a random character from that type to the generated characters list
        selected_type = random.choice([char_type for char_type, is_selected in zip(charSets.keys(), selected) if is_selected])
        generated.append(random.choice(charSets[selected_type]))

    random.shuffle(generated)
    password = "".join(generated)

    # Display the generated password
    password_text.delete('1.0', tk.END)  # Clear the previous password
    password_text.insert(tk.END, password)

    # Check password strength
    strength = password_strength(password)
    strength_value.set(strength)

def password_strength(password):
    if len(password) <= 8:
        return "Weak"
    if re.search(r"\d|[A-Z]", password) and re.search(r"[\W_]", password):
        return "Strong"
    return "Medium"

# Create the GUI window
window = tk.Tk()
window.title("Python Password Generator")

# Create and pack the password length label and entry
length_label = tk.Label(window, text="Password Length:")
length_label.pack()
length_entry = tk.Entry(window)
length_entry.pack()

# Create the character type checkboxes
checkbox_vars = {}
for char_type in ["Lowercase", "Uppercase", "Numbers", "Symbols"]:
    checkbox_vars[char_type] = tk.IntVar(value=1)
    checkbox = tk.Checkbutton(window, text=char_type, variable=checkbox_vars[char_type])
    checkbox.pack(anchor=tk.W)

# Create and pack the generate button
generate_button = tk.Button(window, text="Generate Password", command=generate_password)
generate_button.pack()

# Create and pack the generated password label
password_label = tk.Label(window, text="Generated password:")
password_label.pack()

# Create a Text widget to display the generated password with text wrapping
password_text = tk.Text(window, wrap=tk.WORD, height=1, width=20)
password_text.pack()

# Create and pack the copy button with proper error handling
copy_button = tk.Button(window, text="Copy", command=lambda: copy_password())
copy_button.pack()

def copy_password():
    try:
        password_to_copy = password_text.get('1.0', tk.END)
        pyperclip.copy(password_to_copy)
    except pyperclip.PyperclipException:
        error_label.config(text="Your system does not support the clipboard")

# Create and pack the password strength label
strength_value = tk.StringVar()
strength_label = tk.Label(window, text="Password strength:")
strength_label.pack()
strength_display = tk.Label(window, textvariable=strength_value)
strength_display.pack()

# Create a mini-red label for possible errors
error_label = tk.Label(window, fg="red", text="")
error_label.pack()

# Start the GUI event loop
window.mainloop()
