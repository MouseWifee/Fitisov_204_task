import tkinter as tk
from tkinter import ttk, messagebox
from app.models.task import Task


class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task: Task | None = None):
        super().__init__(parent)
        self.result = None
        self.task = task
        self.title("Редактировать задачу" if task else "Новая задача")
        self.geometry("460x520")
        self.resizable(False, False)
        self.configure(bg="#f4f7fb")
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Редактирование" if task else "Добавить задачу", style="Heading.TLabel").pack(anchor="w", pady=(0, 18))
        ttk.Label(frame, text="Название задачи *").pack(anchor="w")
        self.title_var = tk.StringVar(value=task.title if task else "")
        ttk.Entry(frame, textvariable=self.title_var).pack(fill="x", pady=(5, 13))

        ttk.Label(frame, text="Описание").pack(anchor="w")
        self.description = tk.Text(frame, height=4, wrap="word", relief="flat", font=("Segoe UI", 10),
                                   highlightthickness=1, highlightbackground="#dce3ed")
        self.description.pack(fill="x", pady=(5, 13))
        if task:
            self.description.insert("1.0", task.description)

        ttk.Label(frame, text="Приоритет").pack(anchor="w")
        self.priority_var = tk.StringVar(value=task.priority if task else "Средний")
        ttk.Combobox(frame, textvariable=self.priority_var,
                     values=["Низкий", "Средний", "Высокий"], state="readonly").pack(fill="x", pady=(5, 13))
        ttk.Label(frame, text="Срок (ГГГГ-ММ-ДД), необязательно").pack(anchor="w")
        self.due_var = tk.StringVar(value=task.due_date if task else "")
        ttk.Entry(frame, textvariable=self.due_var).pack(fill="x", pady=(5, 16))
        ttk.Button(frame, text="Сохранить задачу", style="Accent.TButton", command=self._save).pack(fill="x")
        self.bind("<Escape>", lambda _: self.destroy())
        self.wait_visibility()
        self.focus_set()

    def _save(self):
        result = Task(id=self.task.id if self.task else None,
                      created_at=self.task.created_at if self.task else "",
                      completed=self.task.completed if self.task else False,
                      title=self.title_var.get().strip(),
                      description=self.description.get("1.0", "end").strip(),
                      priority=self.priority_var.get(), due_date=self.due_var.get().strip())
        try:
            result.validate()
        except ValueError as exc:
            messagebox.showwarning("Проверьте данные", str(exc), parent=self)
            return
        self.result = result
        self.destroy()
