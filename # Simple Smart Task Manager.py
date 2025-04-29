# Simple Smart Task Manager

from datetime import datetime  # For handling completion date

# List to store tasks
tasks = []

# Function to add a new task
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    priority = input("Enter priority (low, medium, high): ")
    
    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
        "status": "pending",
        "completed_date": None  # Initially not completed
    }
    
    tasks.append(task)
    print(f"✅ Task '{title}' added successfully!")

# Function to list all tasks
def list_tasks():
    if not tasks:
        print("⚠ No tasks available.")
        return
    
    print("\n📌 Tasks:")
    for i, task in enumerate(tasks, start=1):
        status = f"✅ Completed on {task['completed_date']}" if task["status"] == "completed" else "❌ Pending"
        print(f"{i}. {task['title']} (Priority: {task['priority']}) - Due: {task['due_date']} - {status}")

# Function to mark a task as completed
def mark_task_completed():
    list_tasks()
    
    if not tasks:
        return

    try:
        task_number = int(input("\nEnter the task number to mark as completed: ")) - 1
        if 0 <= task_number < len(tasks):
            if tasks[task_number]["status"] == "completed":
                print("⚠ Task is already completed!")
            else:
                tasks[task_number]["status"] = "completed"
                tasks[task_number]["completed_date"] = datetime.now().strftime("%Y-%m-%d")
                print(f"✅ Task '{tasks[task_number]['title']}' marked as completed on {tasks[task_number]['completed_date']}!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Function to delete a task
def delete_task():
    list_tasks()
    
    if not tasks:
        return

    try:
        task_number = int(input("\nEnter the task number to delete: ")) - 1
        if 0 <= task_number < len(tasks):
            removed_task = tasks.pop(task_number)
            print(f"🗑 Task '{removed_task['title']}' deleted successfully!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Main menu function
def main():
    while True:
        print("\n📋 Simple Task Manager")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            mark_task_completed()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("👋 Exiting Task Manager. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# Run the task manager
if __name__ == "__main__":
    main()
