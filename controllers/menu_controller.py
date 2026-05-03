from models.task_manager import TaskManager
from models.task import Task
from views.console_view import ConsoleView

class MenuController:
    def __init__(self):
        self.manager = TaskManager()
        self.view = ConsoleView()
        self.running = True

    def run(self):
        self.view.show_message("Welcome to Task Manager")
        self.manager.load_from_json()
        while self.running:
            self.view.show_menu()
            cmd = input("\nYour choice: ").strip()
            {
                '1': self._add,
                '2': self._view_all,
                '3': self._edit,
                '4': self._delete,
                '5': self._filter,
                '6': self._undo,
                '7': self._queue,
                '8': self._save,
                '9': self._load,
                '0': self._exit
            }.get(cmd, lambda: self.view.show_message("Invalid", True))()

    def _add(self):
        title, desc, prio = self.view.get_task_details()
        t = Task(title, desc, prio)
        if self.manager.add_task(t):
            self.view.show_message(f"Added: {title}")

    def _view_all(self):
        self.view.show_tasks(self.manager.get_tasks(), "All tasks")

    def _edit(self):
        tasks = self.manager.get_tasks()
        t = self.view.select_task(tasks, "edit")
        if not t:
            return
        updates = self.view.get_edit_details(t)
        if updates and self.manager.update_task(t.id, **updates):
            self.view.show_message("Updated")

    def _delete(self):
        tasks = self.manager.get_tasks()
        t = self.view.select_task(tasks, "delete")
        if t and self.manager.remove_task(t.id):
            self.view.show_message("Deleted")

    def _filter(self):
        status, priority = self.view.get_filter()
        if status is None and priority is None:
            return
        res = self.manager.get_tasks(status, priority)
        self.view.show_tasks(res, "Filtered")

    def _undo(self):
        if self.manager.undo():
            self.view.show_message("Undo OK")
        else:
            self.view.show_message("Nothing to undo", True)

    def _queue(self):
        self.view.show_priority_queue(self.manager.get_priority_queue())

    def _save(self):
        if self.manager.save_to_json():
            self.view.show_message("Saved to data/tasks.json")

    def _load(self):
        if self.manager.load_from_json():
            self.view.show_message("Loaded from JSON")
        else:
            self.view.show_message("No saved file", True)

    def _exit(self):
        self.view.show_message("Bye!")
        self.running = False
