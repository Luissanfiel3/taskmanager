from asyncio import tasks
import json

class Task:

    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.description}"


class TaskManager:

    FILENAME = "Task.json"

    def __init__(self):
        self._task = []
        self._next_id = 1
        self.load_task()

    def add_task(self, description):
        task = Task(self._next_id, description)
        self._task.append(task)
        self._next_id += 1
        print(f"Tarea añadida {description}")
        self.save_task()

    def list_task(self):
        if not self._task:
            print("No hay tareas pendientes")
        else:
            for task in self._task:
                print(task)

    def complete_task(self, id):
        for task in self._task:
            if task.id == int(id):
                task.completed = True
                print(f"Tarea completada {task}")
                self.save_task()
                return
        print(f"Tarea no encontrada #{id}")

    def delete_task(self, id):
        for task in self._task:
            if task.id == int(id):
                self._task.remove(task)
                print(f"Tarea eliminada {task}")
                self.save_task()
                return
        print(f"Tarea no encontrada #{id}")

    def load_task(self):
        try:
            with open(self.FILENAME, "r") as file:
                data = json.load(file)
                self._task = [Task(item["id"], item ["description"], item["completed"]) for item in data]
                if self._task:
                     self._next_id = self._task[-1].id + 1
                else:
                    self._next_id = 1

        except FileNotFoundError:
            self._task = []

    def save_task(self):
        with open(self.FILENAME, "w") as file:
            json.dump([{"id": task.id, "description": task.description, "completed": task.completed} for task in self._task], file, indent=4)
