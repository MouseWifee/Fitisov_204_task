import tkinter as tk
from tkinter import ttk, messagebox
from app.services.task_service import TaskService
from app.ui.task_dialog import TaskDialog


class MainWindow(tk.Tk):
    def __init__(self, service: TaskService):
        super().__init__()
        self.service = service
        self.title("TaskFlow — Планировщик задач")
        self.geometry("1030x660")
        self.minsize(850, 550)
        self.configure(bg="#f4f7fb")
        self._configure_style()
        self._create_widgets()
        self.refresh()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f7fb")
        style.configure("TLabel", background="#f4f7fb", foreground="#243248", font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 21, "bold"), foreground="#182b48")
        style.configure("TButton", font=("Segoe UI", 10), padding=(13, 9), borderwidth=0)
        style.configure("Accent.TButton", background="#316bdf", foreground="white")
        style.map("Accent.TButton", background=[("active", "#2459c6")])
        style.configure("TEntry", padding=7)
        style.configure("TCombobox", padding=6)
        style.configure("Treeview", rowheight=45, font=("Segoe UI", 10), background="white",
                        fieldbackground="white", foreground="#26364c", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=13,
                        background="#e8eef8", foreground="#33465e")
        style.map("Treeview", background=[("selected", "#d7e7ff")], foreground=[("selected", "#203552")])

    def _create_widgets(self):
        container = ttk.Frame(self, padding=(28, 25))
        container.pack(fill="both", expand=True)
        top = ttk.Frame(container)
        top.pack(fill="x")
        ttk.Label(top, text="TaskFlow", style="Heading.TLabel").pack(side="left")
        ttk.Button(top, text="+  Новая задача", style="Accent.TButton", command=self.add_task).pack(side="right")
        ttk.Label(container, text="Ваши дела в одном месте. Планируйте, выполняйте, отмечайте результат.").pack(anchor="w", pady=(4, 23))

        stats = ttk.Frame(container)
        stats.pack(fill="x", pady=(0, 25))
        self.stat_labels = []
        for title, color in [("ВСЕГО ЗАДАЧ", "#316bdf"), ("В РАБОТЕ", "#d98a26"), ("ВЫПОЛНЕНО", "#1e9a70")]:
            outer = tk.Frame(stats, bg="white", highlightbackground="#e0e8f2", highlightthickness=1)
            outer.pack(side="left", fill="x", expand=True, padx=(0, 12))
            tk.Label(outer, text=title, bg="white", fg="#7b8a9e", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18, pady=(15, 1))
            count = tk.Label(outer, text="0", bg="white", fg=color, font=("Segoe UI", 27, "bold"))
            count.pack(anchor="w", padx=18, pady=(0, 13))
            self.stat_labels.append(count)

        controls = ttk.Frame(container)
        controls.pack(fill="x", pady=(0, 14))
        ttk.Label(controls, text="Список задач", font=("Segoe UI", 14, "bold")).pack(side="left", padx=(0, 22))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh())
        ttk.Entry(controls, textvariable=self.search_var, width=31).pack(side="left", padx=(0, 12))
        self.filter_var = tk.StringVar(value="Все задачи")
        filter_box = ttk.Combobox(controls, textvariable=self.filter_var, state="readonly", width=16,
                                  values=["Все задачи", "Активные", "Выполненные"])
        filter_box.pack(side="left")
        filter_box.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        frame = ttk.Frame(container)
        frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(frame, columns=("title", "priority", "due", "status"), show="headings", selectmode="browse")
        for col, text, width, anchor in [("title", "ЗАДАЧА", 450, "w"), ("priority", "ПРИОРИТЕТ", 130, "center"),
                                         ("due", "СРОК", 140, "center"), ("status", "СТАТУС", 150, "center")]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor, minwidth=75)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<Double-1>", lambda _: self.edit_task())
        self.tree.tag_configure("done", foreground="#8a98a9")

        footer = ttk.Frame(container)
        footer.pack(fill="x", pady=(15, 0))
        ttk.Button(footer, text="Изменить", command=self.edit_task).pack(side="left", padx=(0, 8))
        ttk.Button(footer, text="Выполнено / Вернуть", command=self.toggle_task).pack(side="left", padx=(0, 8))
        ttk.Button(footer, text="Удалить", command=self.delete_task).pack(side="left")
        ttk.Label(footer, text="Двойной щелчок по задаче — редактирование", foreground="#8290a2").pack(side="right")

    def refresh(self):
        selected = self.tree.selection()
        selected_id = selected[0] if selected else None
        for row in self.tree.get_children():
            self.tree.delete(row)
        self._tasks_by_id = {}
        for task in self.service.list_tasks(self.search_var.get(), self.filter_var.get()):
            self._tasks_by_id[str(task.id)] = task
            self.tree.insert("", "end", iid=str(task.id), values=(task.title, task.priority,
                task.due_date or "—", "Готово" if task.completed else "В работе"),
                tags=("done",) if task.completed else ())
        if selected_id and self.tree.exists(selected_id):
            self.tree.selection_set(selected_id)
        for label, number in zip(self.stat_labels, self.service.statistics()):
            label.config(text=str(number))

    def _selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Выберите задачу", "Сначала выберите задачу в таблице.", parent=self)
            return None
        return self._tasks_by_id[selection[0]]

    def add_task(self):
        dialog = TaskDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            t = dialog.result
            self.service.create(t.title, t.description, t.priority, t.due_date)
            self.refresh()

    def edit_task(self):
        task = self._selected()
        if task is None:
            return
        dialog = TaskDialog(self, task)
        self.wait_window(dialog)
        if dialog.result:
            self.service.edit(dialog.result)
            self.refresh()

    def toggle_task(self):
        task = self._selected()
        if task is not None:
            task.completed = not task.completed
            self.service.edit(task)
            self.refresh()

    def delete_task(self):
        task = self._selected()
        if task is not None and messagebox.askyesno("Удаление", f"Удалить задачу «{task.title}»?", parent=self):
            self.service.remove(task.id)
            self.refresh()
