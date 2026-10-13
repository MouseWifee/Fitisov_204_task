# TaskFlow

TaskFlow — приложение для управления задачами на Python. Интерфейс сделан с помощью Tkinter, для хранения данных используется SQLite.


## Структура проекта

- `app/models` — модель задачи и проверка данных
- `app/repositories` — интерфейс репозитория и работа с SQLite
- `app/services` — операции с задачами
- `app/ui` — главное окно и форма задачи
- `tests` — тесты
- `main.py` — запуск приложения


```bash
python main.py
```

Тесты:

```bash
python -m unittest discover -s tests -v
```

## Скриншоты

### Главное окно

![Главное окно](screenshots/01_main_window.png)

### Редактирование задачи

![Редактирование задачи](screenshots/02_edit_task.png)

### Выполненные задачи

![Фильтр выполненных задач](screenshots/03_completed_filter.png)
