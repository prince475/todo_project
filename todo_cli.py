import pytest
from todo.todo import ToDoList
import os

FILENAME = "tasks.json"

def run_tests():
    print("Running tests...\n")

    # Create a custom pytest hook to capture test result details
    class TestResult:
        def pytest_runtest_logreport(self, report):
            if report.when == "call":
                if report.outcome == "passed":
                    print(f"[PASSED] {report.nodeid}")
                elif report.outcome == "failed":
                    print(f"[FAILED] {report.nodeid}")
                    print(f"    Reason: {report.longrepr}")

    # Run the tests with the custom result output handler
    result = pytest.main(["--tb=short", "--disable-warnings"], plugins=[TestResult()])
    
    if result == 0:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed. See above for details.")

def main():
    todo_list = ToDoList()

    # Load tasks from file if it exists
    if os.path.exists(FILENAME):
        todo_list.load_from_file(FILENAME)

    while True:

        todo_list.show_tasks()

        print("\nOptions:")
        print("1. Add Task")
        print("2. Mark Task Complete")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Filter Tasks")
        print("6. Run Tests")
        print("7. Save and Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            description = input("Task description (optional): ").strip()
            due_date = input("Due date (YYYY-MM-DD, optional): ").strip() or None
            priority = input("Priority (Low, Medium, High, optional): ").strip() or "Medium"
            category = input("Category (e.g., Work, Personal, optional): ").strip() or "General"
            try:
                todo_list.add_task(title, description, due_date, priority, category)
                print("Task added successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            task_id = int(input("Enter task ID to mark complete: "))
            try:
                todo_list.mark_complete(task_id)
                print("Task marked as complete!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            task_id = int(input("Enter task ID to update: "))
            title = input("New title (leave blank to keep current): ").strip() or None
            description = input("New description (leave blank to keep current): ").strip() or None
            due_date = input("New due date (YYYY-MM-DD, leave blank to keep current): ").strip() or None
            priority = input("New priority (Low, Medium, High, leave blank to keep current): ").strip() or None
            category = input("New category (leave blank to keep current): ").strip() or None
            try:
                todo_list.update_task(task_id, title, description, due_date, priority, category)
                print("Task updated successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            task_id = int(input("Enter task ID to delete: "))
            try:
                todo_list.delete_task(task_id)
                print("Task deleted successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            filter_by = input("Filter by (priority, category, due_date): ").strip()
            value = input("Enter value to filter by: ").strip()
            filtered_tasks = todo_list.get_tasks(filter_by, value)
            print("\nFiltered Tasks:")
            for task in filtered_tasks:
                print(task)

        elif choice == "6":
            run_tests()

        elif choice == "7":
            todo_list.save_to_file(FILENAME)
            print("Tasks saved. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
