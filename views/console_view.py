from models.task import Priority, Status

class ConsoleView:
    @staticmethod
    def show_menu():
        print("\n" + "="*50)
        print("📋 TASK MANAGER")
        print("="*50)
        print("1. ➕ Add task")
        print("2. 📋 View all")
        print("3. ✏️ Edit task")
        print("4. 🗑️ Delete task")
        print("5. 🔍 Filter tasks")
        print("6. ⏪ Undo")
        print("7. 📊 Priority queue")
        print("8. 💾 Save to JSON")
        print("9. 📂 Load from JSON")
        print("0. 🚪 Exit")

    @staticmethod
    def get_text(prompt):
        while True:
            val = input(prompt).strip()
            if val:
                return val
            print("❌ Cannot be empty")

    @staticmethod
    def get_task_details():
        print("\n📝 New task:")
        title = ConsoleView.get_text("Title: ")
        desc = input("Description: ").strip()
        print("Priority: 1.Low 2.Medium 3.High")
        while True:
            try:
                p = int(input("Choose (1-3): "))
                if p == 1:
                    prio = Priority.LOW
                elif p == 2:
                    prio = Priority.MEDIUM
                elif p == 3:
                    prio = Priority.HIGH
                else:
                    continue
                break
            except:
                print("Enter 1,2,3")
        return title, desc, prio

    @staticmethod
    def show_tasks(tasks, title="Tasks"):
        print(f"\n📌 {title}:")
        if not tasks:
            print("  No tasks")
            return
        for i, t in enumerate(tasks, 1):
            print(f"{i}. [{t.priority.value}] {t.title} | {t.status.value}")
            print(f"   ID: {t.id}")
            print(f"   {t.description[:60]}")
            print("-"*40)

    @staticmethod
    def select_task(tasks, action):
        if not tasks:
            print("No tasks")
            return None
        ConsoleView.show_tasks(tasks, f"Select to {action}")
        while True:
            try:
                idx = int(input(f"Number (1-{len(tasks)}): "))
                if 1 <= idx <= len(tasks):
                    return tasks[idx-1]
            except:
                pass
            print(f"Enter 1..{len(tasks)}")

    @staticmethod
    def get_filter():
        print("\n1. By status  2. By priority  3. Both  0. Cancel")
        ch = input("Choice: ")
        if ch == "0":
            return None, None
        status = None
        priority = None
        if ch in ["1","3"]:
            print("Status: 1.Todo 2.InProgress 3.Done")
            s = input(": ")
            if s == "1": status = Status.TODO
            elif s == "2": status = Status.IN_PROGRESS
            elif s == "3": status = Status.DONE
        if ch in ["2","3"]:
            print("Priority: 1.Low 2.Medium 3.High")
            p = input(": ")
            if p == "1": priority = Priority.LOW
            elif p == "2": priority = Priority.MEDIUM
            elif p == "3": priority = Priority.HIGH
        return status, priority

    @staticmethod
    def get_edit_details(task):
        print(f"\nEditing: {task.title}")
        title = input(f"Title [{task.title}]: ").strip()
        desc = input(f"Description: ").strip()
        updates = {}
        if title:
            updates['title'] = title
        if desc:
            updates['description'] = desc
        return updates

    @staticmethod
    def show_message(msg, is_error=False):
        prefix = "❌" if is_error else "✅"
        print(f"{prefix} {msg}")

    @staticmethod
    def show_priority_queue(queue):
        print("\n📊 Priority queue (High→Low):")
        if not queue:
            print("  Empty")
            return
        for i, t in enumerate(queue, 1):
            print(f"{i}. [{t.priority.value}] {t.title}")
