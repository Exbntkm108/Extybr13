import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        # Поля ввода
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.pages_var = tk.StringVar()

        tk.Label(root, text="Название книги").pack()
        tk.Entry(root, textvariable=self.title_var).pack()

        tk.Label(root, text="Автор").pack()
        tk.Entry(root, textvariable=self.author_var).pack()

        tk.Label(root, text="Жанр").pack()
        tk.Entry(root, textvariable=self.genre_var).pack()

        tk.Label(root, text="Количество страниц").pack()
        tk.Entry(root, textvariable=self.pages_var).pack()

        # Кнопка добавления книги
        self.add_button = tk.Button(root, text="Добавить книгу", command=self.add_book)
        self.add_button.pack()

        # Таблица книг
        self.book_list = ttk.Treeview(root, columns=("title", "author", "genre", "pages"), show="headings")
        self.book_list.heading("title", text="Название книги")
        self.book_list.heading("author", text="Автор")
        self.book_list.heading("genre", text="Жанр")
        self.book_list.heading("pages", text="Количество страниц")
        self.book_list.pack()

        # Фильтрация
        tk.Label(root, text="Фильтр по жанру").pack()
        self.genre_filter_var = tk.StringVar()
        tk.Entry(root, textvariable=self.genre_filter_var).pack()
        filter_button = tk.Button(root, text="Применить фильтр", command=self.filter_books)
        filter_button.pack()

        self.data = []
        self.load_data()

    def add_book(self):
        title = self.title_var.get()
        author = self.author_var.get()
        genre = self.genre_var.get()
        pages = self.pages_var.get()

        # Проверка корректности ввода
        if not self.validate_input(title, author, genre, pages):
            return

        self.data.append({"title": title, "author": author, "genre": genre, "pages": int(pages)})
        self.book_list.insert("", "end", values=(title, author, genre, pages))
        self.save_data()

    def validate_input(self, title, author, genre, pages):
        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Ни одно из полей не должно быть пустым.")
            return False

        try:
            pages = int(pages)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом.")
            return False

        return True

    def filter_books(self):
        genre_filter = self.genre_filter_var.get()
        for item in self.book_list.get_children():
            self.book_list.delete(item)

        for book in self.data:
            if genre_filter.lower() in book['genre'].lower() or not genre_filter:
                self.book_list.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_data(self):
        with open("books.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                self.data = json.load(f)
                for book in self.data:
                    self.book_list.insert("", "end",
                                          values=(book["title"], book["author"], book["genre"], book["pages"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()