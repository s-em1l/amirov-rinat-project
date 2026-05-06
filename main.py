import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Амиров Ринат")
        self.books = []
        self.load_data()

        # UI Setup
        input_frame = tk.LabelFrame(root, text="Добавить книгу", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(input_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.genre_entry = tk.Entry(input_frame)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Кол-во страниц:").grid(row=3, column=0, sticky="w")
        self.pages_entry = tk.Entry(input_frame)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=2)

        self.add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Filter Section
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre_entry = tk.Entry(filter_frame)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=2)

        self.more_than_200_var = tk.BooleanVar()
        self.filter_pages_check = tk.Checkbutton(filter_frame, text="Только более 200 страниц", variable=self.more_than_200_var)
        self.filter_pages_check.grid(row=1, column=0, columnspan=2, sticky="w")

        self.filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.update_display)
        self.filter_btn.grid(row=2, column=0, padx=5, pady=5)
        
        self.reset_btn = tk.Button(filter_frame, text="Сбросить", command=self.reset_filters)
        self.reset_btn.grid(row=2, column=1, padx=5, pady=5)

        # Table Section
        table_frame = tk.Frame(root)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страницы")
        
        self.tree.column("Title", width=150)
        self.tree.column("Author", width=120)
        self.tree.column("Genre", width=100)
        self.tree.column("Pages", width=80)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.update_display()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_raw = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages_raw:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            pages = int(pages_raw)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом!")
            return

        self.books.append({
            "Title": title,
            "Author": author,
            "Genre": genre,
            "Pages": pages
        })
        self.save_data()
        self.update_display()
        self.clear_entries()
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    def reset_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.more_than_200_var.set(False)
        self.update_display()

    def update_display(self):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_genre = self.filter_genre_entry.get().strip().lower()
        filter_200 = self.more_than_200_var.get()

        for book in self.books:
            # Genre filter
            if filter_genre and filter_genre not in book["Genre"].lower():
                continue
            
            # Pages filter (> 200)
            if filter_200 and book["Pages"] <= 200:
                continue

            self.tree.insert("", "end", values=(book["Title"], book["Author"], book["Genre"], book["Pages"]))

    def save_data(self):
        try:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

    def load_data(self):
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except Exception:
                self.books = []

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    app = BookTrackerApp(root)
    root.mainloop()
