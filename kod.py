import tkinter as tk
from tkinter import messagebox, ttk
import json
import random
import os

# Пути к файлам
QUOTES_FILE = "quotes.json"
HISTORY_FILE = "history.json"

# Загрузка данных из JSON
def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# Сохранение данных в JSON
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Генерация случайной цитаты
def generate_quote():
    if not quotes:
        messagebox.showwarning("Нет цитат", "База цитат пуста. Добавьте новые цитаты.")
        return
    quote = random.choice(quotes)
    history.append(quote)
    save_json(history, HISTORY_FILE)
    update_history_list()
    quote_label.config(text=f'"{quote["text"]}"\n— {quote["author"]}')

# Обновление списка истории
def update_history_list():
    history_listbox.delete(0, tk.END)
    for q in history:
        history_listbox.insert(tk.END, f'"{q["text"]}" — {q["author"]}')

# Фильтрация по автору/теме
def filter_quotes():
    author = author_var.get()
    theme = theme_var.get()
    filtered = [q for q in quotes if (not author or q["author"] == author) and (not theme or q["theme"] == theme)]
    quote_label.config(text="Фильтр применён. Выберите цитату из истории или сгенерируйте новую.")
    # Для простоты фильтрация только в истории отображения, генерация — из полной базы

# Добавление новой цитаты
def add_quote():
    text = entry_text.get().strip()
    author = entry_author.get().strip()
    theme = entry_theme.get().strip()
    if not text or not author or not theme:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    new_quote = {"text": text, "author": author, "theme": theme}
    quotes.append(new_quote)
    save_json(quotes, QUOTES_FILE)
    messagebox.showinfo("Успех", "Цитата добавлена!")
    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_theme.delete(0, tk.END)

# Инициализация данных
quotes = load_json(QUOTES_FILE)
history = load_json(HISTORY_FILE)

# Создание окна
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")
root.resizable(False, False)

# Виджеты
quote_label = tk.Label(root, text="Нажмите 'Сгенерировать', чтобы получить цитату", wraplength=500, justify="center", font=("Arial", 12))
quote_label.pack(pady=10)

generate_btn = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_btn.pack(pady=5)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
author_var = tk.StringVar()
author_combo = ttk.Combobox(filter_frame, textvariable=author_var, values=list(set(q["author"] for q in quotes)))
author_combo.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
theme_var = tk.StringVar()
theme_combo = ttk.Combobox(filter_frame, textvariable=theme_var, values=list(set(q["theme"] for q in quotes)))
theme_combo.grid(row=0, column=3, padx=5)

filter_btn = tk.Button(filter_frame, text="Фильтровать", command=filter_quotes)
filter_btn.grid(row=0, column=4, padx=5)

# История
history_label = tk.Label(root, text="История сгенерированных цитат:")
history_label.pack(pady=5)
history_listbox = tk.Listbox(root, width=70, height=10)
history_listbox.pack(pady=5)
update_history_list()

# Добавление новой цитаты
add_frame = tk.Frame(root)
add_frame.pack(pady=15)
tk.Label(add_frame, text="Текст:").grid(row=0, column=0, padx=5)
entry_text = tk.Entry(add_frame, width=40)
entry_text.grid(row=0, column=1, padx=5)
tk.Label(add_frame, text="Автор:").grid(row=1, column=0, padx=5)
entry_author = tk.Entry(add_frame, width=40)
entry_author.grid(row=1, column=1, padx=5)
tk.Label(add_frame, text="Тема:").grid(row=2, column=0, padx=5)
entry_theme = tk.Entry(add_frame, width=40)
entry_theme.grid(row=2, column=1, padx=5)
add_btn = tk.Button(add_frame, text="Добавить цитату", command=add_quote)
add_btn.grid(row=3, columnspan=2, pady=10)

root.mainloop()