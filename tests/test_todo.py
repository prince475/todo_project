import pytest
from todo.todo import ToDoList, Task
from datetime import datetime

import os
import json
import re 

@pytest.fixture
def todo_list():
    return ToDoList()

def test_add_task(todo_list):
    task = todo_list.add_task("Task 1", "Description", due_date="2024-12-10", priority="High", category="Work")
    assert task.title == "Task 1"
    assert task.description == "Description"
    assert task.priority == "High"
    assert task.category == "Work"
    assert task.due_date == datetime.strptime("2024-12-10", "%Y-%m-%d")
    assert not task.completed

def test_get_tasks_with_filter(todo_list):
    todo_list.add_task("Task 1", "Description 1", priority="High", category="Work")
    todo_list.add_task("Task 2", "Description 2", priority="Low", category="Personal")
    todo_list.add_task("Task 3", "Description 3", priority="High", category="Personal")

    high_priority_tasks = todo_list.get_tasks(filter_by="priority", value="High")
    assert len(high_priority_tasks) == 2
    assert all(task.priority == "High" for task in high_priority_tasks)

    personal_tasks = todo_list.get_tasks(filter_by="category", value="Personal")
    assert len(personal_tasks) == 2
    assert all(task.category == "Personal" for task in personal_tasks)

def test_update_task(todo_list):
    task = todo_list.add_task("Task 1", "Description")
    updated_task = todo_list.update_task(task.id, title="Updated Task", priority="Low", due_date="2024-12-15")
    assert updated_task.title == "Updated Task"
    assert updated_task.priority == "Low"
    assert updated_task.due_date == datetime.strptime("2024-12-15", "%Y-%m-%d")

def test_mark_complete(todo_list):
    task = todo_list.add_task("Task 1", "Description")
    assert not task.completed
    completed_task = todo_list.mark_complete(task.id)
    assert completed_task.completed

def test_delete_task(todo_list):
    task = todo_list.add_task("Task 1", "Description")
    todo_list.delete_task(task.id)
    assert len(todo_list.get_tasks()) == 0

def test_save_and_load(todo_list, tmp_path):
    task1 = todo_list.add_task("Task 1", "Description 1", priority="High", category="Work")
    task2 = todo_list.add_task("Task 2", "Description 2", priority="Low", category="Personal")
    task1.mark_complete()

    file_path = tmp_path / "tasks.json"
    todo_list.save_to_file(str(file_path))

    new_todo_list = ToDoList()
    new_todo_list.load_from_file(str(file_path))
    
    loaded_tasks = new_todo_list.get_tasks()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0].title == "Task 1"
    assert loaded_tasks[0].completed
    assert loaded_tasks[1].priority == "Low"
    assert loaded_tasks[1].category == "Personal"

def test_task_string_representation(todo_list):
    task = todo_list.add_task("Task 1", "Description", due_date="2024-12-10", priority="High", category="Work")
    assert str(task) == "[ ] Task 1 (Priority: High, Category: Work, Due: 2024-12-10)"
    task.mark_complete()
    assert str(task) == "[X] Task 1 (Priority: High, Category: Work, Due: 2024-12-10)"

def test_task_validation(todo_list):
    task = todo_list.add_task("Task 9", "Description", due_date="2024-12-10", priority="High", category="Work")
    
    # Check if title is non-empty
    assert task.title != "", "Task title should not be empty"
    
    # Check if the title matches a specific pattern (e.g., starts with "Task")
    assert re.match(r"^Task", task.title), "Task title should start with 'Task'"
    
    # Check if the description is non-empty
    assert task.description != "", "Task description should not be empty"
    
    # Check if the due date is a valid date
    assert isinstance(task.due_date, datetime), "Task due date should be a datetime object"
    
    # Check if the priority is valid (e.g., High, Low, Medium)
    assert task.priority in ["High", "Low", "Medium"], f"Invalid priority: {task.priority}"
    
    # Check if the task is not completed initially
    assert not task.completed, "New tasks should not be completed"
