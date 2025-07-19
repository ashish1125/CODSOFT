import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import datetime
import json
import os

TASK_FILE = "tasks.json"
tasks = []
displayed_task_indices = []

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, default=str)

def parse_deadline(deadline_str):
    return datetime.datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")

def refresh_task_list():
    global displayed_task_indices
    task_listbox.delete(*task_listbox.get_children())
    now = datetime.datetime.now()
    indexed_tasks = list(enumerate(tasks))
    sorted_tasks = sorted(indexed_tasks, key=lambda t: parse_deadline(t[1]['deadline']))
    displayed_task_indices = []

    for display_index, (original_index, task) in enumerate(sorted_tasks):
        deadline = parse_deadline(task['deadline'])
        if task['completed']:
            time_left = "✔ Done"
        elif deadline < now:
            time_left = "⚠️ Missed"
        else:
            time_left = str(deadline - now).split('.')[0]

        task_listbox.insert("", "end", iid=display_index, values=(
            task['name'],
            task['deadline'],
            time_left,
            "Yes" if task['completed'] else "No"
        ))

        if not task['completed'] and deadline < now:
            task_listbox.item(display_index, tags=("missed",))

        displayed_task_indices.append(original_index)

    task_listbox.tag_configure("missed", foreground="red")

def add_task():
    TaskDialog("Add Task", save_new_task)

def save_new_task(name, date_obj, hour, minute):
    deadline = datetime.datetime.combine(date_obj, datetime.time(int(hour), int(minute)))
    task = {"name": name, "deadline": deadline.strftime("%Y-%m-%d %H:%M"), "completed": False}
    tasks.append(task)
    save_tasks()
    refresh_task_list()

def update_task():
    selected = task_listbox.selection()
    if not selected:
        messagebox.showwarning("Select Task", "No task selected.")
        return
    idx = displayed_task_indices[int(selected[0])]
    task = tasks[idx]
    TaskDialog("Update Task", lambda n, d, h, m: update_task_data(idx, n, d, h, m), initial=task)

def update_task_data(index, name, date_obj, hour, minute):
    deadline = datetime.datetime.combine(date_obj, datetime.time(int(hour), int(minute)))
    tasks[index]['name'] = name
    tasks[index]['deadline'] = deadline.strftime("%Y-%m-%d %H:%M")
    save_tasks()
    refresh_task_list()

def toggle_complete():
    selected = task_listbox.selection()
    if not selected:
        return
    idx = displayed_task_indices[int(selected[0])]
    tasks[idx]['completed'] = not tasks[idx]['completed']
    save_tasks()
    refresh_task_list()

def delete_task():
    selected = task_listbox.selection()
    if not selected:
        return
    idx = displayed_task_indices[int(selected[0])]
    confirm = messagebox.askyesno("Delete", f"Delete '{tasks[idx]['name']}'?")
    if confirm:
        tasks.pop(idx)
        save_tasks()
        refresh_task_list()

class TaskDialog(tk.Toplevel):
    def __init__(self, title, on_submit, initial=None):
        super().__init__()
        self.title(title)
        self.on_submit = on_submit
        self.initial = initial
        self.geometry("300x250")
        self.resizable(False, False)

        tk.Label(self, text="Task Name").pack(pady=(10, 2))
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.pack()

        tk.Label(self, text="Select Date").pack(pady=(10, 2))
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.date_entry.pack()

        time_frame = tk.Frame(self)
        time_frame.pack(pady=10)

        tk.Label(time_frame, text="Hour").pack(side=tk.LEFT)
        self.hour_var = tk.StringVar()
        hour_menu = ttk.Combobox(time_frame, textvariable=self.hour_var, values=[f"{i:02}" for i in range(24)], width=3)
        hour_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(time_frame, text="Minute").pack(side=tk.LEFT)
        self.minute_var = tk.StringVar()
        minute_menu = ttk.Combobox(time_frame, textvariable=self.minute_var, values=[f"{i:02}" for i in range(60)], width=3)
        minute_menu.pack(side=tk.LEFT)

        tk.Button(self, text="Save", command=self.submit).pack(pady=15)

        if initial:
            self.name_entry.insert(0, initial['name'])
            dt = parse_deadline(initial['deadline'])
            self.date_entry.set_date(dt.date())
            self.hour_var.set(f"{dt.hour:02}")
            self.minute_var.set(f"{dt.minute:02}")

    def submit(self):
        name = self.name_entry.get()
        if not name or not self.hour_var.get() or not self.minute_var.get():
            messagebox.showerror("Invalid", "Please fill in all fields.")
            return
        self.on_submit(name, self.date_entry.get_date(), self.hour_var.get(), self.minute_var.get())
        self.destroy()

# GUI Setup
root = tk.Tk()
root.title("📝 To-Do List")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

columns = ("Task", "Deadline", "Time Left", "Completed")
task_listbox = ttk.Treeview(frame, columns=columns, show="headings", height=10)
for col in columns:
    task_listbox.heading(col, text=col)
    task_listbox.column(col, width=150)
task_listbox.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="➕ Add Task", width=15, command=add_task).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="✏️ Update Task", width=15, command=update_task).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="✔  Task Status", width=15, command=toggle_complete).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="🗑 Delete Task", width=15, command=delete_task).grid(row=0, column=3, padx=5)

# Load and display
tasks = load_tasks()
refresh_task_list()
root.mainloop()
