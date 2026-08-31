import json
import os
import argparse
import csv
from datetime import datetime

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

def add_task(description, category="General"):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    
    new_task = {
        "id": new_id, 
        "task": description, 
        "category": category,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added: '{description}' in category '{category}'")

def view_tasks(show_all=False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Enjoy your day!")
        return
    
    print("\n--- Your Tasks ---")
    for t in tasks:
        # If show_all is False, only show pending tasks
        if not show_all and t['status'] == 'completed':
            continue
            
        status_icon = "✅" if t['status'] == "completed" else "⏳"
        print(f"[{t['id']}] {status_icon} ({t['category']}) {t['task']} - Created: {t['created_at']}")
    print("------------------\n")

def complete_task(task_id):
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = 'completed'
            found = True
            break
            
    if found:
        save_tasks(tasks)
        print(f"🎉 Task {task_id} marked as completed!")
    else:
        print(f"⚠️ No task found with ID {task_id}.")

def export_tasks_to_csv():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to export.")
        return
        
    csv_file = "tasks_export.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Task", "Category", "Status", "Created At"])
        for t in tasks:
            writer.writerow([t['id'], t['task'], t['category'], t['status'], t['created_at']])
            
    print(f"📊 Tasks successfully exported to {csv_file}. Ready for Excel/Power BI analysis!")

def delete_task(task_id):
    tasks = load_tasks()
    filtered_tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) == len(filtered_tasks):
        print(f"⚠️ No task found with ID {task_id}.")
    else:
        save_tasks(filtered_tasks)
        print(f"🗑️ Task {task_id} permanently deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An Advanced CLI Task Manager")
    parser.add_argument("action", choices=["add", "view", "complete", "delete", "export"], help="The action you want to perform")
    parser.add_argument("--task", type=str, help="The task description (for 'add')")
    parser.add_argument("--category", type=str, default="General", help="Task category (optional for 'add')")
    parser.add_argument("--id", type=int, help="The task ID (for 'complete' or 'delete')")
    parser.add_argument("--all", action="store_true", help="View all tasks including completed ones (for 'view')")

    args = parser.parse_args()

    if args.action == "add":
        if args.task:
            add_task(args.task, args.category)
        else:
            print("Error: --task argument is required when adding a task.")
    elif args.action == "view":
        view_tasks(show_all=args.all)
    elif args.action == "complete":
        if args.id:
            complete_task(args.id)
        else:
            print("Error: --id argument is required to complete a task.")
    elif args.action == "delete":
        if args.id:
            delete_task(args.id)
        else:
            print("Error: --id argument is required to delete a task.")
    elif args.action == "export":
        export_tasks_to_csv()