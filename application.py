import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("700x500")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f7f7f7")  # Default light background

        # Variables for theme
        self.light_theme = {"bg": "#f7f7f7", "fg": "#333"}
        self.dark_theme = {"bg": "#2e2e2e", "fg": "#f7f7f7"}
        self.current_theme = self.light_theme

        # Fonts
        heading_font = ("Helvetica", 16, "bold")
        text_font = ("Helvetica", 12)

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabs for All Tasks and Completed Tasks
        self.all_tasks_tab = ttk.Frame(self.notebook)
        self.completed_tasks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.all_tasks_tab, text="All Tasks")
        self.notebook.add(self.completed_tasks_tab, text="Completed Tasks")

        # Title Label
        title_label = tk.Label(self.all_tasks_tab, text="My To-Do List", font=heading_font, bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        title_label.pack(pady=10)

        # Frame for task display
        frame = tk.Frame(self.all_tasks_tab, bg=self.current_theme["bg"])
        frame.pack(pady=10, expand=True, fill="both")

        # Task display with scrollbar
        self.task_listbox = tk.Listbox(frame, height=15, width=60, selectmode=tk.SINGLE, font=text_font, bg="#ffffff", fg=self.current_theme["fg"])
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        # Task Entry and Deadline Entry
        self.task_entry = ttk.Entry(self.all_tasks_tab, width=40, font=text_font)
        self.task_entry.pack(pady=5)

        self.deadline_entry = ttk.Entry(self.all_tasks_tab, width=40, font=text_font)
        self.deadline_entry.pack(pady=5)
        self.deadline_entry.insert(0, "YYYY-MM-DD")  # Placeholder for deadline format

        # Total Tasks Label
        self.total_tasks_label = tk.Label(self.all_tasks_tab, text="Total Tasks: 0", font=text_font, bg=self.current_theme["bg"], fg=self.current_theme["fg"])
        self.total_tasks_label.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.all_tasks_tab, bg=self.current_theme["bg"])
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Mark as Done", command=self.mark_task_done).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Clear All Tasks", command=self.clear_all_tasks).grid(row=1, column=0, columnspan=3, pady=10)

        # Dark Mode Toggle
        ttk.Button(button_frame, text="Toggle Theme", command=self.toggle_theme).grid(row=2, column=0, columnspan=3, pady=5)

        # Quit Button
        ttk.Button(button_frame, text="Quit", command=root.quit).grid(row=3, column=0, columnspan=3, pady=5)

        # Initialize task list
        self.tasks = []

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == self.light_theme:
            self.current_theme = self.dark_theme
        else:
            self.current_theme = self.light_theme

        self.root.configure(bg=self.current_theme["bg"])
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.current_theme["bg"], fg=self.current_theme["fg"])

    def add_task(self):
        """Add a new task to the list with an optional deadline."""
        task = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return

        # Validate deadline
        if deadline and deadline != "YYYY-MM-DD":
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
                        index = self.task_listbox.size()
                        self.task_listbox.insert(tk.END, f"{status} {task['name']} (Due: {deadline_str})")
                        self.task_listbox.itemconfig(index, {'fg': 'red'})
                    else:
                        self.task_listbox.insert(tk.END, f"{status} {task['name']} (Due: {deadline_str})")
                else:
                    self.task_listbox.insert(tk.END, f"{status} {task['name']} (No deadline)")

        # Update the total tasks label
        self.total_tasks_label.config(text=f"Total Tasks: {len(self.tasks)}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()