import json
import os
import tempfile
import unittest
from unittest.mock import patch

from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = os.path.join(self.temp_dir.name, "tasks.json")
        self.filename_patch = patch.object(TaskManager, "FILENAME", self.filename)
        self.filename_patch.start()

    def tearDown(self):
        self.filename_patch.stop()
        self.temp_dir.cleanup()

    def test_starts_empty_when_file_does_not_exist(self):
        manager = TaskManager()

        self.assertEqual(manager._task, [])
        self.assertEqual(manager._next_id, 1)

    def test_add_task_assigns_id_and_persists(self):
        manager = TaskManager()

        manager.add_task("Estudiar Python")

        self.assertEqual(len(manager._task), 1)
        self.assertEqual(manager._task[0].id, 1)
        self.assertEqual(manager._task[0].description, "Estudiar Python")
        self.assertFalse(manager._task[0].completed)

        with open(self.filename, encoding="utf-8") as file:
            saved_tasks = json.load(file)
        self.assertEqual(saved_tasks[0]["description"], "Estudiar Python")

    def test_load_task_restores_tasks_and_next_id(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([
                {"id": 4, "description": "Leer", "completed": True},
            ], file)

        manager = TaskManager()

        self.assertEqual(len(manager._task), 1)
        self.assertEqual(manager._task[0].id, 4)
        self.assertTrue(manager._task[0].completed)
        self.assertEqual(manager._next_id, 5)

    def test_load_task_simulates_saved_tasks_without_using_task_json(self):
        simulated_tasks = [
            {"id": 7, "description": "Tarea simulada", "completed": False},
            {"id": 8, "description": "Tarea completada", "completed": True},
        ]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(simulated_tasks, file)

        manager = TaskManager()

        self.assertEqual(
            [(task.id, task.description, task.completed) for task in manager._task],
            [(7, "Tarea simulada", False), (8, "Tarea completada", True)],
        )
        self.assertEqual(manager._next_id, 9)

    def test_complete_task_marks_matching_task(self):
        manager = TaskManager()
        manager.add_task("Leer")

        manager.complete_task("1")

        self.assertTrue(manager._task[0].completed)

    def test_complete_task_keeps_tasks_when_id_does_not_exist(self):
        manager = TaskManager()
        manager.add_task("Leer")

        manager.complete_task("99")

        self.assertEqual(len(manager._task), 1)
        self.assertFalse(manager._task[0].completed)

    def test_delete_task_removes_matching_task(self):
        manager = TaskManager()
        manager.add_task("Leer")

        manager.delete_task("1")

        self.assertEqual(manager._task, [])

    def test_delete_task_keeps_tasks_when_id_does_not_exist(self):
        manager = TaskManager()
        manager.add_task("Leer")

        manager.delete_task("99")

        self.assertEqual(len(manager._task), 1)

    def test_invalid_id_raises_value_error(self):
        manager = TaskManager()
        manager.add_task("Leer")

        with self.assertRaises(ValueError):
            manager.complete_task("abc")

        with self.assertRaises(ValueError):
            manager.delete_task("abc")


if __name__ == "__main__":
    unittest.main()
