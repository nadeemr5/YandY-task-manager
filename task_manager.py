import json
from datetime import datetime
from abc import ABC, abstractmethod

# Exception Handling
class InvalidInputError(Exception):
    pass

# Base Task Class
class Task(ABC):
    def __init__(self, title, description, due_date, priority="low", status="pending"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_completed(self):
        self.status = "completed"

    @abstractmethod
    def __str__(self):
        pass

# Basic Task Class
class BasicTask(Task):
    def __str__(self):
        return (
            f"Task: {self.title}\n"
            f"Description: {self.description}\n"
            f"Due Date: {self.due_date.strftime('%Y-%m-%d')}\n"
            f"Priority: {self.priority}\n"
            f"Status: {self.status}"
        )

# Recurring Task Class
class RecurringTask(Task):
    def __init__(self, title, description, due_date, recurrence="weekly", priority="low"):
        super().__init__(title, description, due_date, priority)
        self.recurrence = recurrence

    def __str__(self):
        return (
            f"Task: {self.title}\n"
            f"Description: {self.description}\n"
            f"Due Date: {self.due_date.strftime('%Y-%m-%d')}\n"
            f"Priority: {self.priority}\n"
            f"Status: {self.status}\n"
            f"Recurrence: {self.recurrence}"
        )

# Deadline Task Class
class DeadlineTask(Task):
    def __init__(self, title, description, due_date, priority="high"):
        super().__init__(title, description, due_date, priority)

    def __str__(self):
        return (
            f"Task: {self.title}\n"
            f"Description: {self.description}\n"
            f"Due Date: {self.due_date.strftime('%Y-%m-%d')}\n"
            f"Priority: {self.priority}\n"
            f"Status: {self.status}\n"
            f"Type: Deadline Task"
        )

# User Class
class User:
    def __init__(self, username, password):
        self.username = username
        self._password = password  # Encapsulation
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def __str__(self):
        return f"User: {self.username}"

# Database Handler for File Handling
class DatabaseHandler:
    @staticmethod
    def save_tasks(users, filename="tasks.json"):
        data = []
        for user in users:
            user_data = {
                "username": user.username,
                "tasks": [
                    {
                        "title": task.title,
                        "description": task.description,
                        "due_date": task.due_date.strftime("%Y-%m-%d"),
                        "priority": task.priority,
                        "status": task.status,
                        "type": task.__class__.__name__
                    }
                    for task in user.get_tasks()
                ]
            }
            data.append(user_data)
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_tasks(filename="tasks.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                users = []
                for user_data in data:
                    user = User(user_data["username"], "dummy_password")
                    for task_data in user_data["tasks"]:
                        task_class = globals()[task_data["type"]]
                        task = task_class(
                            title=task_data["title"],
                            description=task_data["description"],
                            due_date=datetime.strptime(task_data["due_date"], "%Y-%m-%d"),
                            priority=task_data["priority"]
                        )
                        task.status = task_data["status"]
                        user.add_task(task)
                    users.append(user)
                return users
        except FileNotFoundError:
            return []

# Task Manager Class
class TaskManager:
    def __init__(self):
        self.users = DatabaseHandler.load_tasks()

    def add_user(self, user):
        self.users.append(user)

    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def list_all_tasks(self):
        for user in self.users:
            print(user)
            for task in user.get_tasks():
                print(task)
                print("-" * 40)

    def search_tasks(self, username, keyword):
        user = self.find_user(username)
        if user:
            return [task for task in user.get_tasks() if keyword.lower() in task.title.lower()]
        return []

    def filter_tasks(self, username, status):
        user = self.find_user(username)
        if user:
            return [task for task in user.get_tasks() if task.status == status]
        return []

    def save_data(self):
        DatabaseHandler.save_tasks(self.users)

# CLI Interface
def main():
    task_manager = TaskManager()

    while True:
        print("\nSmart Task Manager")
        print("1. Add User")
        print("2. Add Task")
        print("3. List All Tasks")
        print("4. Mark Task as Completed")
        print("5. Search Tasks")
        print("6. Filter Tasks by Status")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(username, password)
            task_manager.add_user(user)
            print(f"User '{username}' added successfully!")

        elif choice == "2":
            username = input("Enter username: ")
            user = task_manager.find_user(username)
            if user:
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                due_date = input("Enter due date (YYYY-MM-DD): ")
                priority = input("Enter priority (low/medium/high): ")
                task_type = input("Enter task type (basic/recurring/deadline): ")

                try:
                    due_date = datetime.strptime(due_date, "%Y-%m-%d")
                    if task_type == "basic":
                        task = BasicTask(title, description, due_date, priority)
                    elif task_type == "recurring":
                        recurrence = input("Enter recurrence (weekly/monthly): ")
                        task = RecurringTask(title, description, due_date, recurrence, priority)
                    elif task_type == "deadline":
                        task = DeadlineTask(title, description, due_date, priority)
                    else:
                        raise InvalidInputError("Invalid task type.")
                    user.add_task(task)
                    print("Task added successfully!")
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                except InvalidInputError as e:
                    print(e)
            else:
                print("User not found.")

        elif choice == "3":
            task_manager.list_all_tasks()

        elif choice == "4":
            username = input("Enter username: ")
            user = task_manager.find_user(username)
            if user:
                task_title = input("Enter task title to mark as completed: ")
                for task in user.get_tasks():
                    if task.title == task_title:
                        task.mark_as_completed()
                        print(f"Task '{task_title}' marked as completed.")
                        break
                else:
                    print("Task not found.")
            else:
                print("User not found.")

        elif choice == "5":
            username = input("Enter username: ")
            keyword = input("Enter search keyword: ")
            results = task_manager.search_tasks(username, keyword)
            if results:
                for task in results:
                    print(task)
                    print("-" * 40)
            else:
                print("No tasks found.")

        elif choice == "6":
            username = input("Enter username: ")
            status = input("Enter status to filter by (pending/completed): ")
            results = task_manager.filter_tasks(username, status)
            if results:
                for task in results:
                    print(task)
                    print("-" * 40)
            else:
                print("No tasks found.")

        elif choice == "7":
            task_manager.save_data()
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()