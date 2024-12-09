from datetime import datetime
from typing import List, Optional

class Task:
    task_counter = 0

    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None, priority: str = "Medium", category: str = "General"):
        if not title:
            raise ValueError("Title cannot be empty")
        Task.task_counter += 1
        self.id = Task.task_counter
        self.title = title
        self.description = description
        self.completed = False
        self.priority = priority
        self.category = category
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        due = f", Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else ""
        return f"[{'X' if self.completed else ' '}] {self.title} (Priority: {self.priority}, Category: {self.category}{due})"


class ToDoList:
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, title: str, description: str = "", due_date: Optional[str] = None, priority: str = "Medium", category: str = "General"):
        task = Task(title, description, due_date, priority, category)
        self.tasks.append(task)
        return task

    def get_tasks(self, filter_by: Optional[str] = None, value: Optional[str] = None):
        filtered_tasks = self.tasks
        if filter_by == "priority":
            filtered_tasks = [task for task in self.tasks if task.priority == value]
        elif filter_by == "category":
            filtered_tasks = [task for task in self.tasks if task.category == value]
        elif filter_by == "due_date":
            filtered_tasks = [task for task in self.tasks if task.due_date and task.due_date.strftime("%Y-%m-%d") == value]

        return filtered_tasks

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[str] = None, priority: Optional[str] = None, category: Optional[str] = None):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Task not found")
        if title:
            task.title = title
        if description:
            task.description = description
        if due_date:
            task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        if priority:
            task.priority = priority
        if category:
            task.category = category
        return task

    def delete_task(self, task_id: int):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Task not found")
        self.tasks.remove(task)

    def mark_complete(self, task_id: int):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("Task not found")
        task.mark_complete()
        return task

    def save_to_file(self, filename: str):
        with open(filename, "w") as file:
            tasks_data = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "category": task.category,
                    "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else None,
                }
                for task in self.tasks
            ]
            import json
            json.dump(tasks_data, file)

    def load_from_file(self, filename: str):
        import json
        with open(filename, "r") as file:
            tasks_data = json.load(file)
            for data in tasks_data:
                task = self.add_task(data["title"], data["description"], data["due_date"], data["priority"], data["category"])
                if data["completed"]:
                    task.mark_complete()

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            print("\n--- To-Do List ---")
            for task in self.tasks:
                print(task)
