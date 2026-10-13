from pathlib import Path
from app.repositories.sqlite_repository import SQLiteTaskRepository
from app.services.task_service import TaskService
from app.ui.main_window import MainWindow


def main() -> None:
    database = Path(__file__).resolve().parent / "data" / "tasks.db"
    repository = SQLiteTaskRepository(database)
    service = TaskService(repository)
    MainWindow(service).mainloop()


if __name__ == "__main__":
    main()
