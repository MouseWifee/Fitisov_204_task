"""Запуск: python -m unittest discover -s tests -v"""
import tempfile
import unittest
from pathlib import Path
from app.repositories.sqlite_repository import SQLiteTaskRepository
from app.services.task_service import TaskService


class TaskServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.service = TaskService(SQLiteTaskRepository(Path(self.temp.name) / "test.db"))

    def tearDown(self):
        self.temp.cleanup()

    def test_create_and_statistics(self):
        self.service.create("Купить продукты", "Молоко", "Средний", "")
        self.assertEqual(self.service.statistics(), (1, 1, 0))

    def test_filter_and_complete(self):
        self.service.create("Учеба", "", "Высокий", "2026-10-18")
        task = self.service.list_tasks()[0]
        task.completed = True
        self.service.edit(task)
        self.assertEqual(len(self.service.list_tasks(status="Активные")), 0)
        self.assertEqual(len(self.service.list_tasks(status="Выполненные")), 1)

    def test_title_validation(self):
        with self.assertRaises(ValueError):
            self.service.create("   ", "", "Средний", "")

    def test_search_and_delete(self):
        self.service.create("Подготовить презентацию", "", "Средний", "")
        task = self.service.list_tasks(search="презентац")[0]
        self.service.remove(task.id)
        self.assertEqual(self.service.statistics(), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
