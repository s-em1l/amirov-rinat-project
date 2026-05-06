import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import urllib.request
from PIL import Image, ImageTk
import io

class GitHubUserFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder - Амиров Ринат")
        
        self.favorites = []
        self.load_favorites()

        # UI Setup
        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Search Section
        search_frame = tk.LabelFrame(main_frame, text="Поиск пользователя", padx=10, pady=10)
        search_frame.pack(fill="x", pady=5)

        tk.Label(search_frame, text="Логин GitHub:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        self.search_btn = tk.Button(search_frame, text="Найти", command=self.search_user)
        self.search_btn.pack(side="left")

        # Result Section
        self.result_frame = tk.LabelFrame(main_frame, text="Результат поиска", padx=10, pady=10)
        self.result_frame.pack(fill="x", pady=5)
        
        self.user_info_label = tk.Label(self.result_frame, text="Введите имя для поиска", justify="left")
        self.user_info_label.pack(side="left", padx=10)
        
        self.add_fav_btn = tk.Button(self.result_frame, text="В избранное", command=self.add_to_favorites, state="disabled")
        self.add_fav_btn.pack(side="right")

        self.current_user = None

        # Favorites Section
        fav_frame = tk.LabelFrame(main_frame, text="Избранные пользователи", padx=10, pady=10)
        fav_frame.pack(fill="both", expand=True, pady=5)

        self.tree = ttk.Treeview(fav_frame, columns=("Login", "Name", "Repos", "Bio"), show='headings')
        self.tree.heading("Login", text="Логин")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Repos", text="Репозитории")
        self.tree.heading("Bio", text="Био")
        
        self.tree.column("Login", width=100)
        self.tree.column("Name", width=120)
        self.tree.column("Repos", width=100)
        self.tree.column("Bio", width=200)
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(fav_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.update_display()

    def search_user(self):
        username = self.search_entry.get().strip()
        if not username:
            messagebox.showerror("Ошибка", "Введите логин для поиска!")
            return

        try:
            # GitHub API request
            req = urllib.request.Request(f"https://api.github.com/users/{username}")
            # Add user-agent to avoid 403
            req.add_header('User-Agent', 'Python-Urllib')
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
            self.current_user = {
                "Login": data.get("login"),
                "Name": data.get("name") or "N/A",
                "Repos": data.get("public_repos"),
                "Bio": data.get("bio") or "No bio provided"
            }
            
            info_text = f"Логин: {self.current_user['Login']}\n" \
                        f"Имя: {self.current_user['Name']}\n" \
                        f"Репозитории: {self.current_user['Repos']}\n" \
                        f"Био: {self.current_user['Bio'][:50]}..."
            
            self.user_info_label.config(text=info_text)
            self.add_fav_btn.config(state="normal")
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                messagebox.showerror("Ошибка", "Пользователь не найден.")
            else:
                messagebox.showerror("Ошибка", f"Ошибка API: {e.code}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def add_to_favorites(self):
        if not self.current_user:
            return
            
        # Check if already in favorites
        if any(u["Login"] == self.current_user["Login"] for u in self.favorites):
            messagebox.showinfo("Инфо", "Пользователь уже в избранном!")
            return
            
        self.favorites.append(self.current_user)
        self.save_favorites()
        self.update_display()
        messagebox.showinfo("Успех", f"{self.current_user['Login']} добавлен в избранное!")

    def update_display(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for u in self.favorites:
            self.tree.insert("", "end", values=(u["Login"], u["Name"], u["Repos"], u["Bio"]))

    def save_favorites(self):
        try:
            with open("favorites.json", "w", encoding="utf-8") as f:
                json.dump(self.favorites, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_favorites(self):
        if os.path.exists("favorites.json"):
            try:
                with open("favorites.json", "r", encoding="utf-8") as f:
                    self.favorites = json.load(f)
            except:
                self.favorites = []

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    app = GitHubUserFinderApp(root)
    root.mainloop()
