import json
import os
import argparse

FILE_NAME = 'tasks.json'

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "task": description})
    save_tasks(tasks)
    print(f"✅ Task added: '{description}'")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Enjoy your day!")
        return
    print("\n--- Your Tasks ---")
    for t in tasks:
        print(f"[{t['id']}] {t['task']}")
    print("------------------\n")

def delete_task(task_id):
    tasks = load_tasks()
    filtered_tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) == len(filtered_tasks):
        print(f"⚠️ No task found with ID {task_id}.")
    else:
        save_tasks(filtered_tasks)
        print(f"🗑️ Task {task_id} deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI Task Manager")
    parser.add_argument("action", choices=["add", "view", "delete"], help="The action you want to perform")
    parser.add_argument("--task", type=str, help="The task description (required for 'add')")
    parser.add_argument("--id", type=int, help="The task ID (required for 'delete')")

    args = parser.parse_args()

    if args.action == "add":
        if args.task:
            add_task(args.task)
        else:
            print("Error: --task argument is required when adding a task.")
    elif args.action == "view":
        view_tasks()
    elif args.action == "delete":
        if args.id:
            delete_task(args.id)
        else:
            print("Error: --id argument is required when deleting a task.")