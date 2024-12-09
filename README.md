# To-Do CLI Project

A simple, interactive command-line interface (CLI) application for managing a to-do list. This project includes task management features such as adding, updating, deleting, and filtering tasks, as well as robust testing with pytest. Continuous Integration (CI) is implemented using GitHub Actions.

## Features

- Add tasks with title, description, due date, priority, and category.
- Update tasks and mark them as complete.
- Delete tasks by ID.
- View tasks with optional filtering by priority, category, or completion status.
- Save tasks to a JSON file and load them on startup.
- Dynamic validation to ensure task data integrity.
- Integrated pytest testing with coverage reporting.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/<your-username>/todo-cli.git
    cd todo-cli
    ```

2. Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the CLI tool:

```bash
python main.py
```
## Commands

| Command                   | Description                                   |
| ------------------------- | --------------------------------------------- |
| `add`                      | Add a new task                               |
| `update <task_id>`         | Update an existing task                      |
| `delete <task_id>`         | Delete a task by ID                          |
| `list`                     | List all tasks                               |
| `filter <criteria>`        | List tasks based on filters                  |
| `mark-complete <task_id>`  | Mark a task as complete                      |

## Testing
The project uses pytest for unit and integration tests. You can run the tests 
locally with the following command:
```bash
pytest
```

For testing specific features, you can also run individual test files:
```bash
pytest test_todo.py
```
## Dynamic Task Validation Tests

We added validation to ensure task attributes like title, description, due date, 
and priority follow specific rules. If the task fails any validation checks, the 
test will provide specific failure messages.

Edge Cases that can be tested include:
1. Empty task titles and Invalid priorities

```python
def test_task_validation(todo_list):
    # Test adding a task with a valid title and priority
    task = todo_list.add_task("Task 1", "Description", due_date="2024-12-10", priority="High", category="Work")
    assert task.title != "", "Task title should not be empty"
    assert re.match(r"^Task", task.title), "Task title should start with 'Task'"
    assert isinstance(task.due_date, datetime), "Task due date should be a datetime object"
    assert task.priority in ["High", "Low", "Medium"], f"Invalid priority: {task.priority}"

    # Test adding a task with an empty title
    try:
        todo_list.add_task("", "Description", due_date="2024-12-10", priority="High", category="Work")
        assert False, "Adding a task with an empty title should raise an exception"
    except ValueError as e:
        assert str(e) == "Title cannot be empty"

    # Test adding a task with an invalid priority
    try:
        todo_list.add_task("Invalid Task", "Description", due_date="2024-12-10", priority="Super High", category="Work")
        assert False, "Adding a task with an invalid priority should raise an exception"
    except ValueError as e:
        assert str(e) == "Invalid priority: Super High"
```
2. Task list operations (adding, updating, filtering) with an empty task list

```python
def test_operations_on_empty_task_list(todo_list):
    # Test filtering tasks when no tasks exist
    filtered_tasks = todo_list.get_tasks(filter_by="priority", value="High")
    assert len(filtered_tasks) == 0, "Filtering on an empty list should return an empty result"

    # Test updating a nonexistent task
    try:
        todo_list.update_task("nonexistent_id", title="New Title")
        assert False, "Updating a nonexistent task should raise a ValueError"
    except ValueError as e:
        assert str(e) == "Task not found"

    # Test deleting a nonexistent task
    try:
        todo_list.delete_task("nonexistent_id")
        assert False, "Deleting a nonexistent task should raise a ValueError"
    except ValueError as e:
        assert str(e) == "Task not found"
```
3. Loading corrupted or nonexistent files

```python
def test_load_corrupted_file(todo_list, tmp_path):
    corrupted_file = tmp_path / "corrupted_tasks.json"
    corrupted_file.write_text('{"invalid_json": [')  # Write invalid JSON content
    
    try:
        todo_list.load_from_file(str(corrupted_file))
        assert False, "Loading a corrupted file should raise a JSONDecodeError"
    except json.JSONDecodeError:
        pass

def test_load_nonexistent_file(todo_list):
    try:
        todo_list.load_from_file("nonexistent_file.json")
        assert False, "Loading a nonexistent file should raise a FileNotFoundError"
    except FileNotFoundError:
        pass
```

To support these tests, ensure the following updates are in place:

1. Add Validation for Empty Title and Invalid Priority:

```python
def add_task(self, title, description, due_date=None, priority=None, category=None):
    if not title:
        raise ValueError("Title cannot be empty")
    if priority not in ["High", "Low", "Medium", None]:
        raise ValueError(f"Invalid priority: {priority}")
    # Existing implementation
```

2. Raise Exceptions for Nonexistent Tasks:

```python
def update_task(self, task_id, **updates):
    task = next((t for t in self.tasks if t.id == task_id), None)
    if not task:
        raise ValueError("Task not found")
    # Update logic...

def delete_task(self, task_id):
    task = next((t for t in self.tasks if t.id == task_id), None)
    if not task:
        raise ValueError("Task not found")
    self.tasks.remove(task)
```

Run all tests with coverage:

```bash
pytest --maxfail=5 --disable-warnings --cov=todo --cov-report=xml
```

## CI/CD Integration
This project uses GitHub Actions for Continuous Integration (CI):

- Tests are automatically executed on every push or pull request.
- Coverage reports are generated as part of the workflow.
- The results are displayed in the GitHub Actions dashboard.

## Running the Workflow
Push your changes to the repository:

```bash
git push origin main
```
Or manually trigger the workflow from the Actions tab on GitHub.

## Contributing
1. Fork the repository.
2. Create a feature branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
Developed with ❤️ by [Prince Daniel].

