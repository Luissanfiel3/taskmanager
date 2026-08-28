from asyncio import tasks


class Task:

    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed = completed

    def __str__(self):
        status = "✓" if self.completed else " "
        return f"[{status}] #{self.id}: {self.description}"


class TaskManager:

    def __init__(self):
        self._task = []
        self._next_id = 1

    def add_task(self, description):
        task = Task(self._next_id, description)
        self._task.append(task)
        self._next_id += 1
        print(f"Tarea añadida {description}")

    def list_task(self):
        if not self._task:
            print("No hay tareas pendientes")
        else:
            for task in self._task:
                print(task)

    def complete_task(self, id):
        for task in self._task:
            if task.id == id:
                task.completed = True
                print(f"Tarea completada {task}")
                return
        print(f"Tarea no encontrada #{id}")

    def delete_task(self, id):
        for task in self._task:
            if task.id == id:
                self._task.remove(task)
                print(f"Tarea eliminada {task}")
                return
        print(f"Tarea no encontrada #{id}")
