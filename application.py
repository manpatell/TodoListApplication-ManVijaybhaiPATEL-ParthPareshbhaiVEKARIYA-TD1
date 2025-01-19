import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x450")
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
        self.task_listbox = tk.Listbox(frame, height=15, width=60, selectmode=tk.SINGLE, font=text_font, bg="#ffffff", fg="#333")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Task Entry
        self.task_entry = ttk.Entry(root, width=40, font=text_font)
        self.task_entry.pack(pady=5)

        # Deadline Entry
        self.deadline_entry = ttk.Entry(root, width=40, font=text_font)
        self.deadline_entry.pack(pady=5)
        self.deadline_entry.insert(0, "YYYY-MM-DD")  # Placeholder for deadline format

        # Total Tasks Label
        self.total_tasks_label = tk.Label(root, text="Total Tasks: 0", font=text_font, bg="#f7f7f7", fg="#333")
        self.total_tasks_label.pack(pady=5)

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
        """Add a new task to the list with an optional deadline."""
        task = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return

        # Validate deadline
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showwarning("Input Error", "Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            deadline_date = None

        # Add task with deadline
        self.tasks.append({"name": task, "done": False, "deadline": deadline_date})
        self.update_task_listbox()

        # Clear inputs
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, "YYYY-MM-DD")

    def mark_task_done(self):
        """Mark the selected task as done."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["done"] = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def delete_task(self):
        """Delete the selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def clear_all_tasks(self):
        """Clear all tasks from the list."""
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?")
        if confirmation:
            self.tasks.clear()
            self.update_task_listbox()
            messagebox.showinfo("Success", "All tasks have been cleared.")
        else:
            messagebox.showinfo("Canceled", "Operation canceled.")

    def update_task_listbox(self):
        """Update the listbox to display all tasks and refresh the total tasks label."""
        self.task_listbox.delete(0, tk.END)
        today = datetime.now().date()

        if not self.tasks:
            self.task_listbox.insert(tk.END, "No TODO items. Add a task to get started!")
        else:
            for task in self.tasks:
                status = "[✔]" if task["done"] else "[ ]"
                if task["deadline"]:
                    deadline_str = task["deadline"].strftime("%Y-%m-%d")
                    if not task["done"] and task["deadline"] < today:
                        # Overdue task in red
                        self.task_listbox.insert(tk.END, f"{status} {task['name']} (Due: {deadline_str})")
                        self.task_listbox.itemconfig(tk.END, {'fg': 'red'})
                    else:
                        self.task_listbox.insert(tk.END, f"{status} {task['name']} (Due: {deadline_str})")
                else:
                    self.task_listbox.insert(tk.END, f"{status} {task['name']}")

        # Update the total tasks label
        self.total_tasks_label.config(text=f"Total Tasks: {len(self.tasks)}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
