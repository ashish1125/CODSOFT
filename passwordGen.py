import tkinter as tk
from tkinter import messagebox
import random
import string

# Generate password logic
def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError

        chars = ''
        if var_upper.get():
            chars += string.ascii_uppercase
        if var_lower.get():
            chars += string.ascii_lowercase
        if var_digits.get():
            chars += string.digits
        if var_symbols.get():
            chars += string.punctuation

        if not chars:
            messagebox.showwarning("No Character Selected", "Please select at least one character type.")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number for length.")

# Setup GUI window
root = tk.Tk()
root.title("Password Generator")
root.geometry("450x380")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

# Title label
tk.Label(root, text="Password Generator", font=("Helvetica", 18, "bold"), fg="#00ffcc", bg="#2b2b2b").pack(pady=15)

# Frame for inputs
frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=10)

# Password length
tk.Label(frame, text="Password Length:", font=("Helvetica", 12), fg="white", bg="#2b2b2b").grid(row=0, column=0, sticky="w", padx=10, pady=5)
length_entry = tk.Entry(frame, width=10, font=("Helvetica", 12))
length_entry.grid(row=0, column=1, padx=10)

# Checkbuttons
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(frame, text="Include Uppercase (A-Z)", variable=var_upper, font=("Helvetica", 10), fg="white", bg="#2b2b2b", selectcolor="#444444").grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
tk.Checkbutton(frame, text="Include Lowercase (a-z)", variable=var_lower, font=("Helvetica", 10), fg="white", bg="#2b2b2b", selectcolor="#444444").grid(row=2, column=0, columnspan=2, sticky="w", padx=10)
tk.Checkbutton(frame, text="Include Digits (0-9)", variable=var_digits, font=("Helvetica", 10), fg="white", bg="#2b2b2b", selectcolor="#444444").grid(row=3, column=0, columnspan=2, sticky="w", padx=10)
tk.Checkbutton(frame, text="Include Symbols (!@#)", variable=var_symbols, font=("Helvetica", 10), fg="white", bg="#2b2b2b", selectcolor="#444444").grid(row=4, column=0, columnspan=2, sticky="w", padx=10)

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, font=("Helvetica", 12), bg="#00b894", fg="white", activebackground="#00997a", padx=10, pady=5).pack(pady=15)

# Password output field
result_entry = tk.Entry(root, font=("Courier", 14), justify='center', width=30, bd=0, bg="#1e1e1e", fg="#00ffcc")
result_entry.pack(pady=10)

# Run the app
root.mainloop()
