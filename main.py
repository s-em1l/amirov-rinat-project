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

        tk.Label(root, text="Title:").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Author:").grid(row=1, column=0)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(root, text="Genre:").grid(row=2, column=0)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(root, text="Pages:").grid(row=3, column=0)
        self.pages_entry = tk.Entry(root)
        self.pages_entry.grid(row=3, column=1)

        tk.Button(root, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2)

        tk.Label(root, text="Filter Genre:").grid(row=5, column=0)
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=5, column=1)
        tk.Button(root, text="Filter", command=self.update_display).grid(row=6, column=0, columnspan=2)

        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        for col in ("Title", "Author", "Genre", "Pages"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=7, column=0, columnspan=2)

        self.update_display()

    def add_book(self):
        t = self.title_entry.get()
        a = self.author_entry.get()
        g = self.genre_entry.get()
        p = self.pages_entry.get()

        if not t or not a or not g or not p:
            messagebox.showerror("Error", "All fields required")
            return
        try:
            p = int(p)
            if p <= 0: raise ValueError
        except:
            messagebox.showerror("Error", "Pages must be a positive number")
            return

        self.books.append({"Title": t, "Author": a, "Genre": g, "Pages": p})
        self.save_data()
        self.update_display()

    def update_display(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        f_genre = self.filter_genre.get().lower()
        for b in self.books:
            if f_genre and f_genre not in b["Genre"].lower(): continue
            # Filter pages > 200 is also a requirement
            if b["Pages"] > 200:
                self.tree.insert("", "end", values=(b["Title"], b["Author"], b["Genre"], b["Pages"]))
            elif not f_genre: # Just show if no filter
                 self.tree.insert("", "end", values=(b["Title"], b["Author"], b["Genre"], b["Pages"]))

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.books, f)

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                self.books = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
