import tkinter as tk
from tkinter import messagebox

# Main To-Do List application
class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        # Initialize task list
        self.tasks = []

        # Task display
        self.task_listbox = tk.Listbox(root, height=15, width=50, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Entry for adding tasks
        self.task_entry = tk.Entry(root, width=45)
        self.task_entry.grid(row=1, column=0, padx=10, pady=5)

        # Buttons
        add_button = tk.Button(root, text="Add Task", command=self.add_task)
        add_button.grid(row=1, column=1, padx=5)

        mark_done_button = tk.Button(root, text="Mark as Done", command=self.mark_task_done)
        mark_done_button.grid(row=2, column=0, padx=10, pady=5)

        delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=2, column=1, padx=5)

        quit_button = tk.Button(root, text="Quit", command=root.quit)
        quit_button.grid(row=2, column=2, padx=10, pady=5)

    def add_task(self):
        """Add a new task to the list."""
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"name": task, "done": False})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

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

    def update_task_listbox(self):
        """Update the listbox to display all tasks."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[✔]" if task["done"] else "[ ]"
            self.task_listbox.insert(tk.END, f"{status} {task['name']}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
