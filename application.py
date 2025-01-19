import tkinter as tk
from tkinter import ttk, messagebox

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("500x400")
        self.root.configure(bg="#f7f7f7")  # Light background color

        # Fonts
        heading_font = ("Helvetica", 16, "bold")
        text_font = ("Helvetica", 12)

        # Title Label
        title_label = tk.Label(root, text="My To-Do List", font=heading_font, bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        # Frame for the task display
        frame = tk.Frame(root, bg="#f7f7f7")
        frame.pack(pady=10)

        # Task display with Scrollbar
        self.task_listbox = tk.Listbox(frame, height=15, width=50, selectmode=tk.SINGLE, font=text_font, bg="#ffffff", fg="#333")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))
        self.task_listbox.insert(tk.END, "No TODO items. Add a task to get started!")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Task Entry
        self.task_entry = ttk.Entry(root, width=40, font=text_font)
        self.task_entry.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root, bg="#f7f7f7")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Mark as Done", command=self.mark_task_done).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear All Tasks", command=self.clear_all_tasks).grid(row=1, column=0, columnspan=3, pady=10)
        ttk.Button(button_frame, text="Quit", command=root.quit).grid(row=2, column=0, columnspan=3, pady=5)

        # Initialize task list
        self.tasks = []

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            if not self.tasks and self.task_listbox.get(0) == "No TODO items. Add a task to get started!":
                self.task_listbox.delete(0)

            self.tasks.append({"name": task, "done": False})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def mark_task_done(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["done"] = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def clear_all_tasks(self):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?")
        if confirmation:
            self.tasks.clear()
            self.update_task_listbox()
            messagebox.showinfo("Success", "All tasks have been cleared.")
        else:
            messagebox.showinfo("Canceled", "Operation canceled.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        if not self.tasks:
            self.task_listbox.insert(tk.END, "No TODO items. Add a task to get started!")
        else:
            for task in self.tasks:
                status = "[✔]" if task["done"] else "[ ]"
                self.task_listbox.insert(tk.END, f"{status} {task['name']}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
