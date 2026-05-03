from collections import deque
from models.task import Task, Priority, Status
import json
import os

class TaskManager:
    def __init__(self):
        self._tasks = []
        self._priority_queue = deque()
        self._undo_stack = []

    def add_task(self, task):
        self._tasks.append(task)
        self._add_to_priority_queue(task)
        self._undo_stack.append(('add', task))
        return True

    def _add_to_priority_queue(self, task):
        order = {'High': 0, 'Medium': 1, 'Low': 2}
        inserted = False
        for i, t in enumerate(self._priority_queue):
            if order[task.priority.value] < order[t.priority.value]:
                self._priority_queue.insert(i, task)
                inserted = True
                break
        if not inserted:
            self._priority_queue.append(task)

    def remove_task(self, task_id):
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                removed = self._tasks.pop(i)
                self._priority_queue = deque([t for t in self._priority_queue if t.id != task_id])
                self._undo_stack.append(('remove', removed))
                return True
        return False

    def update_task(self, task_id, **kwargs):
        for task in self._tasks:
            if task.id == task_id:
                old_state = task.to_dict()
                if 'title' in kwargs:
                    task.title = kwargs['title']
                if 'description' in kwargs:
                    task.description = kwargs['description']
                if 'priority' in kwargs:
                    task.priority = kwargs['priority']
                if 'status' in kwargs:
                    task.status = kwargs['status']
                self._priority_queue = deque([t for t in self._priority_queue if t.id != task_id])
                self._add_to_priority_queue(task)
                self._undo_stack.append(('update', task_id, old_state))
                return True
        return False

    def undo(self):
        if not self._undo_stack:
            return False
        action = self._undo_stack.pop()
        if action[0] == 'add':
            self.remove_task(action[1].id)
        elif action[0] == 'remove':
            self.add_task(action[1])
        elif action[0] == 'update':
            task_id, old_state = action[1], action[2]
            for t in self._tasks:
                if t.id == task_id:
                    t.title = old_state['title']
                    t.description = old_state['description']
                    t.priority = Priority(old_state['priority'])
                    t.status = Status(old_state['status'])
                    break
        return True

    def get_tasks(self, status=None, priority=None):
        result = self._tasks
        if status:
            result = [t for t in result if t.status == status]
        if priority:
            result = [t for t in result if t.priority == priority]
        return result

    def get_priority_queue(self):
        return list(self._priority_queue)

    def save_to_json(self, filename="data/tasks.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self._tasks], f, indent=2, ensure_ascii=False)
        return True

    def load_from_json(self, filename="data/tasks.json"):
        if not os.path.exists(filename):
            return False
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self._tasks = [Task.from_dict(item) for item in data]
        self._priority_queue = deque()
        for t in self._tasks:
            self._add_to_priority_queue(t)
        return True
