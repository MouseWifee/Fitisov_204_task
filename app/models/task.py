from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    title: str
    description: str = ""
    priority: str = "Средний"
    due_date: str = ""
    completed: bool = False
    id: int | None = None
    created_at: str = ""

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Введите название задачи.")
        if len(self.title) > 100:
            raise ValueError("Название не должно превышать 100 символов.")
        if self.priority not in ("Низкий", "Средний", "Высокий"):
            raise ValueError("Выберите корректный приоритет.")
        if self.due_date:
            try:
                date.fromisoformat(self.due_date)
            except ValueError as exc:
                raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД.") from exc
