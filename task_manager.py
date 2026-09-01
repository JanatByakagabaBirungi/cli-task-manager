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

def add_task(description, category="General", due_date=None):
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    
    # Validate date format if provided
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            return

    new_task = {
        "id": new_id, 
        "task": description, 
        "category": category,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added: '{description}' in category '{category}'")

def view_tasks(show_all=False):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    print("\n--- Your Tasks ---")
    current_date = datetime.now()
    
    for t in tasks:
        if not show_all and t['status'] == 'completed':
            continue
            
        status_icon = "✅" if t['status'] == "completed" else "⏳"
        due_info = ""
        
        if t.get('due_date'):
            due_date_obj = datetime.strptime(t['due_date'], "%Y-%m-%d")
            if t['status'] == 'pending' and due_date_obj < current_date:
                due_info = f" [🚨 OVERDUE: {t['due_date']}]"
            else:
                due_info = f" [Due: {t['due_date']}]"
                
        print(f"[{t['id']}] {status_icon} ({t['category']}) {t['task']}{due_info}")
    print("------------------\n")

def search_tasks(query):
    tasks = load_tasks()
    query = query.lower()
    
    results = [t for t in tasks if query in t['task'].lower() or query in t['category'].lower()]
    
    if not results:
        print(f"🔍 No tasks found matching '{query}'.")
        return
        
    print(f"\n--- Search Results for '{query}' ---")
    for t in results:
        status_icon = "✅" if t['status'] == "completed" else "⏳"
        print(f"[{t['id']}] {status_icon} ({t['category']}) {t['task']}")
    print("------------------------------------\n")

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
        writer.writerow(["ID", "Task", "Category", "Status", "Created At", "Due Date"])
        for t in tasks:
            writer.writerow([t['id'], t['task'], t['category'], t['status'], t['created_at'], t.get('due_date', 'None')])
            
    print(f"📊 Tasks successfully exported to {csv_file}.")

def delete_task(task_id):
    tasks = load_tasks()
    filtered_tasks = [t for t in tasks if t['id'] != task_id]
    
    if len(tasks) == len(filtered_tasks):
        print(f"⚠️ No task found with ID {task_id}.")
    else:
        save_tasks(filtered_tasks)
        print(f"🗑️ Task {task_id} deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An Advanced CLI Task Manager")
    parser.add_argument("action", choices=["add", "view", "complete", "delete", "export", "search"], help="The action you want to perform")
    parser.add_argument("--task", type=str, help="The task description")
    parser.add_argument("--category", type=str, default="General", help="Task category")
    parser.add_argument("--due", type=str, help="Due date (YYYY-MM-DD)")
    parser.add_argument("--id", type=int, help="The task ID")
    parser.add_argument("--query", type=str, help="Search keyword (for 'search')")
    parser.add_argument("--all", action="store_true", help="View all tasks including completed ones")

    args = parser.parse_args()

    if args.action == "add":
        if args.task:
            add_task(args.task, args.category, args.due)
        else:
            print("Error: --task argument is required when adding a task.")
    elif args.action == "view":
        view_tasks(show_all=args.all)
    elif args.action == "search":
        if args.query:
            search_tasks(args.query)
        else:
            print("Error: --query argument is required to search.")
    elif args.action == "complete":
        if args.id:
            complete_task(args.id)
    elif args.action == "delete":
        if args.id:
            delete_task(args.id)
    elif args.action == "export":
        export_tasks_to_csv()