import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import zxcvbn

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")

        self.style = ttk.Style(master)
        self.style.configure('TButton', foreground='black', background='lightgray', font=('Arial', 10))
        self.style.configure('TLabel', foreground='black', font=('Arial', 10))
        self.style.configure('TCheckbutton', foreground='black', font=('Arial', 10))
        self.style.configure('Horizontal.TProgressbar', foreground='blue', background='lightblue')

        self.length_label = ttk.Label(master, text="Password Length:")
        self.length_label.pack()

        self.length_entry = ttk.Entry(master)
        self.length_entry.pack()

        self.strength_label = ttk.Label(master, text="Password Strength:")
        self.strength_label.pack()

        self.strength_scale = ttk.Scale(master, from_=1, to=100, orient=tk.HORIZONTAL, length=200)
        self.strength_scale.set(50)  # Default strength
        self.strength_scale.pack()

        self.add_numbers_var = tk.IntVar()
        self.add_numbers_checkbox = ttk.Checkbutton(master, text="Include Numbers", variable=self.add_numbers_var)
        self.add_numbers_checkbox.pack()

        self.add_special_chars_var = tk.IntVar()
        self.add_special_chars_checkbox = ttk.Checkbutton(master, text="Include Special Characters", variable=self.add_special_chars_var)
        self.add_special_chars_checkbox.pack()

        self.add_uppercase_var = tk.IntVar()
        self.add_uppercase_checkbox = ttk.Checkbutton(master, text="Include Uppercase Letters", variable=self.add_uppercase_var)
        self.add_uppercase_checkbox.pack()

        self.add_lowercase_var = tk.IntVar()
        self.add_lowercase_checkbox = ttk.Checkbutton(master, text="Include Lowercase Letters", variable=self.add_lowercase_var)
        self.add_lowercase_checkbox.pack()

        self.unique_var = tk.IntVar()
        self.unique_checkbox = ttk.Checkbutton(master, text="Generate Unique Passwords", variable=self.unique_var)
        self.unique_checkbox.pack()

        self.generate_button = ttk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.copy_button = ttk.Button(master, text="Copy Password", command=self.copy_password)
        self.copy_button.pack()

        self.clear_button = ttk.Button(master, text="Clear Password", command=self.clear_password)
        self.clear_button.pack()

        self.strength_bar = ttk.Progressbar(master, style='Horizontal.TProgressbar')
        self.strength_bar.pack()

        self.result_label = ttk.Label(master, text="")
        self.result_label.pack()

        self.previous_passwords = set()

    def generate_password(self):
        length = random.randint(8, 16)  # Generate a random length between 8 and 16 characters
        strength = self.strength_scale.get()
        include_numbers = self.add_numbers_var.get()
        include_special_chars = self.add_special_chars_var.get()
        include_uppercase = self.add_uppercase_var.get()
        include_lowercase = self.add_lowercase_var.get()
        unique_password = self.unique_var.get()

        if not (include_numbers or include_special_chars or include_uppercase or include_lowercase):
            messagebox.showerror("Error", "Please select at least one option.")
            return

        password = None
        while password is None or (unique_password and password in self.previous_passwords):
            password = self.generate_secure_password(length, strength, include_numbers, include_special_chars, include_uppercase, include_lowercase)

        self.result_label.config(text=f"Generated Password: {password}")
        self.update_strength_bar(strength)
        self.check_password_strength(password)

        if unique_password:
            self.previous_passwords.add(password)

    def generate_secure_password(self, length=12, strength=50, include_numbers=True, include_special_chars=True, include_uppercase=True, include_lowercase=True):
        characters = ''
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        password = ''
        while len(password) < length:
            password += random.choice(characters)

        return password

    def update_strength_bar(self, strength):
        self.strength_bar['value'] = strength

    def check_password_strength(self, password):
        result = zxcvbn.zxcvbn(password)
        suggestions = result['feedback']['suggestions'] if 'suggestions' in result['feedback'] else []
        if result['score'] == 4:
            messagebox.showinfo("Password Strength", "Password is very strong!")
        elif result['score'] == 3:
            messagebox.showwarning("Password Strength", f"Password is strong, but can be stronger.\nSuggestions: {', '.join(suggestions)}")
        elif result['score'] == 2:
            messagebox.showwarning("Password Strength", f"Password is medium strength.\nSuggestions: {', '.join(suggestions)}")
        elif result['score'] == 1:
            messagebox.showwarning("Password Strength", f"Password is weak.\nSuggestions: {', '.join(suggestions)}")
        else:
            messagebox.showwarning("Password Strength", f"Password is very weak.\nSuggestions: {', '.join(suggestions)}")

    def copy_password(self):
        password = self.result_label.cget("text")
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Password Generator", "Password copied to clipboard!")

    def clear_password(self):
        self.result_label.config(text="")
        self.length_entry.delete(0, tk.END)
        self.strength_scale.set(50)
        self.add_numbers_var.set(0)
        self.add_special_chars_var.set(0)
        self.add_uppercase_var.set(0)
        self.add_lowercase_var.set(0)
        self.unique_var.set(0)
        messagebox.showinfo("Password Generator", "Password cleared!")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
