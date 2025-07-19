import tkinter as tk
from tkinter import messagebox

def press(key):
    current = input_text.get()
    if key in "+-*/":
        if current and current[-1] in "+-*/":
            input_text.set(current[:-1] + key)
            return
    input_text.set(current + str(key))

def calculate():
    try:
        result = str(eval(input_text.get()))
        input_text.set(result)
    except ZeroDivisionError:
        input_text.set("")
        messagebox.showerror("Math Error", "Cannot divide by zero.")
    except Exception:
        input_text.set("")
        messagebox.showerror("Input Error", "Invalid input.")

def clear():
    input_text.set("")

def backspace():
    current = input_text.get()
    input_text.set(current[:-1])

# GUI setup
root = tk.Tk()
root.title("Calculator")
root.geometry("570x360")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

input_text = tk.StringVar()

# Display
entry = tk.Entry(root, textvariable=input_text, font=('Segoe UI', 24),
                 bg="#1e1e1e", fg="white", bd=0, justify="right")
entry.pack(fill="both", ipadx=8, ipady=20, padx=10, pady=10)

# Button Frame
button_frame = tk.Frame(root, bg="#1e1e1e")
button_frame.pack(padx=10, pady=10)

# Final layout
buttons = [
    ['7', '8', '9', '+', '-', 'C'],
    ['6', '5', '4', '*', '/', 'X'],  # X = backspace
    ['1', '2', '3', '0', '.', '=']
]

# Create buttons
for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        def cmd(x=char):
            if x == '=':
                calculate()
            elif x == 'C':
                clear()
            elif x == 'X':
                backspace()
            else:
                press(x)

        btn = tk.Button(button_frame, text=char, font=('Segoe UI', 16, 'bold'),
                        bg="#2d2d2d", fg="white", activebackground="#404040",
                        activeforeground="#00ffcc", bd=0, width=6, height=2,
                        command=cmd)
        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

# Equal column widths
for i in range(6):
    button_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
