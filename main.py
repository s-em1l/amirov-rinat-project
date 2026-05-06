import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import urllib.request

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter - Амиров Ринат")
        
        self.history = []
        self.api_url = "https://open.er-api.com/v6/latest/USD"
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT"]
        
        self.load_history()

        # UI Setup
        main_frame = tk.Frame(root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Converter Section
        conv_frame = tk.LabelFrame(main_frame, text="Конвертация", padx=10, pady=10)
        conv_frame.pack(fill="x", pady=5)

        tk.Label(conv_frame, text="Сумма:").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(conv_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(conv_frame, text="Из:").grid(row=1, column=0, sticky="w")
        self.from_currency = ttk.Combobox(conv_frame, values=self.currencies)
        self.from_currency.set("USD")
        self.from_currency.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(conv_frame, text="В:").grid(row=2, column=0, sticky="w")
        self.to_currency = ttk.Combobox(conv_frame, values=self.currencies)
        self.to_currency.set("RUB")
        self.to_currency.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.convert_btn = tk.Button(conv_frame, text="Конвертировать", command=self.convert, bg="#4CAF50", fg="white")
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.result_label = tk.Label(conv_frame, text="Результат: -", font=("Arial", 12, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2)

        # History Section
        hist_frame = tk.LabelFrame(main_frame, text="История конвертаций", padx=10, pady=10)
        hist_frame.pack(fill="both", expand=True, pady=5)

        self.tree = ttk.Treeview(hist_frame, columns=("Amount", "From", "To", "Result", "Date"), show='headings')
        self.tree.heading("Amount", text="Сумма")
        self.tree.heading("From", text="Из")
        self.tree.heading("To", text="В")
        self.tree.heading("Result", text="Результат")
        self.tree.heading("Date", text="Дата")
        
        for col in ("Amount", "From", "To", "Result", "Date"):
            self.tree.column(col, width=80)
            
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        conv_frame.columnconfigure(1, weight=1)
        self.update_display()

    def convert(self):
        amount_str = self.amount_entry.get().strip()
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()

        if not amount_str:
            messagebox.showerror("Ошибка", "Введите сумму!")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return

        try:
            # Using urllib to avoid external dependencies like 'requests'
            with urllib.request.urlopen(f"https://open.er-api.com/v6/latest/{from_curr}") as response:
                data = json.loads(response.read().decode())
                
            if data["result"] == "success":
                rate = data["rates"][to_curr]
                result = round(amount * rate, 2)
                
                self.result_label.config(text=f"Результат: {result} {to_curr}")
                
                from datetime import datetime
                entry = {
                    "amount": amount,
                    "from": from_curr,
                    "to": to_curr,
                    "result": result,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                self.history.insert(0, entry)
                self.save_history()
                self.update_display()
            else:
                messagebox.showerror("Ошибка API", "Не удалось получить актуальные курсы.")
        except Exception as e:
            messagebox.showerror("Ошибка сети", f"Проверьте интернет-соединение: {e}")

    def update_display(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for h in self.history:
            self.tree.insert("", "end", values=(h["amount"], h["from"], h["to"], h["result"], h["date"]))

    def save_history(self):
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_history(self):
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("550x650")
    app = CurrencyConverterApp(root)
    root.mainloop()
