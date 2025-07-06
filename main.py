import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import os
import subprocess
import shutil
import sys

# DB Setup
conn = sqlite3.connect("books.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        pdf_path TEXT NOT NULL
    )
''')
conn.commit()


class BookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book App")
        self.root.geometry("700x600")
        self.selected_id = None
        self.login_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_page(self):
        self.clear_frame()
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.check_login).pack(pady=10)
        tk.Button(self.root, text="User page", command=self.user_page).pack(pady=10)

    def check_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        if user == "admin" and pwd == "admin":
            self.admin_page()
        elif user == "user" and pwd == "user":
            self.user_page()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def copy_to_pdf_folder(self, original_path):
        folder = "pdf"
        os.makedirs(folder, exist_ok=True)

        filename = os.path.basename(original_path)
        destination = os.path.join(folder, filename)

        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(destination):
            destination = os.path.join(folder, f"{base}_{counter}{ext}")
            counter += 1

        try:
            shutil.copyfile(original_path, destination)
            return destination
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy PDF file: {e}")
            return None

    def download_pdf(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a book to download its PDF.")
            return

        pdf_path = self.admin_pdf_path.get() if hasattr(self, "admin_pdf_path") else self.user_pdf_path.get()
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "PDF file not found.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 initialfile=os.path.basename(pdf_path))
        if save_path:
            try:
                shutil.copyfile(pdf_path, save_path)
                messagebox.showinfo("Success", "PDF downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download PDF: {e}")

    def user_page(self):
        self.clear_frame()

        tk.Label(self.root, text="User Page - Book List", font=("Arial", 16)).pack(pady=10)

        columns = ("ID", "Title", "Author", "PDF Path")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=5)

        self.refresh_tree()

        tk.Label(self.root, text="Title").pack()
        self.user_title = tk.Entry(self.root, width=40)
        self.user_title.pack()

        tk.Label(self.root, text="Author").pack()
        self.user_author = tk.Entry(self.root, width=40)
        self.user_author.pack()

        tk.Label(self.root, text="PDF Path").pack()
        self.user_pdf_path = tk.Entry(self.root, width=40)
        self.user_pdf_path.pack()

        tk.Button(self.root, text="Browse PDF", command=self.browse_pdf_user).pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Add", width=10, command=self.user_add_book).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="View PDF", width=10, command=self.view_pdf).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Download PDF", width=12, command=self.download_pdf).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Logout", width=10, command=self.login_page).grid(row=0, column=3, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected)

    def browse_pdf_user(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.user_pdf_path.delete(0, tk.END)
            self.user_pdf_path.insert(0, file_path)

    def user_add_book(self):
        title = self.user_title.get()
        author = self.user_author.get()
        pdf_path = self.user_pdf_path.get()

        if title and author and pdf_path:
            copied_path = self.copy_to_pdf_folder(pdf_path)
            if copied_path:
                cursor.execute("INSERT INTO books (title, author, pdf_path) VALUES (?, ?, ?)",
                               (title, author, copied_path))
                conn.commit()
                messagebox.showinfo("Success", "Book added.")
                self.user_title.delete(0, tk.END)
                self.user_author.delete(0, tk.END)
                self.user_pdf_path.delete(0, tk.END)
                self.refresh_tree()
        else:
            messagebox.showwarning("Warning", "All fields required.")

    def admin_page(self):
        self.clear_frame()

        tk.Label(self.root, text="Admin Page - Book List", font=("Arial", 16)).pack(pady=10)

        columns = ("ID", "Title", "Author", "PDF Path")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=5)

        self.refresh_tree()

        tk.Label(self.root, text="Title").pack()
        self.admin_title = tk.Entry(self.root, width=40)
        self.admin_title.pack()

        tk.Label(self.root, text="Author").pack()
        self.admin_author = tk.Entry(self.root, width=40)
        self.admin_author.pack()

        tk.Label(self.root, text="PDF Path").pack()
        self.admin_pdf_path = tk.Entry(self.root, width=40)
        self.admin_pdf_path.pack()

        tk.Button(self.root, text="Browse PDF", command=self.browse_pdf_admin).pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Button(frame, text="Add", width=10, command=self.admin_add_book).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Update", width=10, command=self.update_book).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Delete", width=10, command=self.delete_book).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="View PDF", width=10, command=self.view_pdf).grid(row=0, column=3, padx=5)
        tk.Button(frame, text="Logout", width=10, command=self.login_page).grid(row=0, column=4, padx=5)
        tk.Button(frame, text="Download PDF", width=12, command=self.download_pdf).grid(row=0, column=5, padx=5)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected)

    def browse_pdf_admin(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.admin_pdf_path.delete(0, tk.END)
            self.admin_pdf_path.insert(0, file_path)

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        cursor.execute("SELECT * FROM books ORDER BY id DESC")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def admin_add_book(self):
        title = self.admin_title.get()
        author = self.admin_author.get()
        pdf_path = self.admin_pdf_path.get()

        if title and author and pdf_path:
            copied_path = self.copy_to_pdf_folder(pdf_path)
            if copied_path:
                cursor.execute("INSERT INTO books (title, author, pdf_path) VALUES (?, ?, ?)",
                               (title, author, copied_path))
                conn.commit()
                messagebox.showinfo("Success", "Book added.")
                self.admin_title.delete(0, tk.END)
                self.admin_author.delete(0, tk.END)
                self.admin_pdf_path.delete(0, tk.END)
                self.refresh_tree()
        else:
            messagebox.showwarning("Warning", "All fields required.")

    def load_selected(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.selected_id = item["values"][0]
            if hasattr(self, "admin_title"):
                self.admin_title.delete(0, tk.END)
                self.admin_author.delete(0, tk.END)
                self.admin_pdf_path.delete(0, tk.END)
                self.admin_title.insert(0, item["values"][1])
                self.admin_author.insert(0, item["values"][2])
                self.admin_pdf_path.insert(0, item["values"][3])
            elif hasattr(self, "user_title"):
                self.user_title.delete(0, tk.END)
                self.user_author.delete(0, tk.END)
                self.user_pdf_path.delete(0, tk.END)
                self.user_title.insert(0, item["values"][1])
                self.user_author.insert(0, item["values"][2])
                self.user_pdf_path.insert(0, item["values"][3])

    def update_book(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        title = self.admin_title.get()
        author = self.admin_author.get()
        pdf_path = self.admin_pdf_path.get()

        if title and author and pdf_path:
            cursor.execute("UPDATE books SET title=?, author=?, pdf_path=? WHERE id=?",
                           (title, author, pdf_path, self.selected_id))
            conn.commit()
            self.refresh_tree()
            messagebox.showinfo("Success", "Book updated.")
            self.admin_title.delete(0, tk.END)
            self.admin_author.delete(0, tk.END)
            self.admin_pdf_path.delete(0, tk.END)
            self.selected_id = None
        else:
            messagebox.showwarning("Warning", "All fields required.")

    def delete_book(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a book first.")
            return

        if messagebox.askyesno("Confirm", "Delete this book?"):
            cursor.execute("DELETE FROM books WHERE id=?", (self.selected_id,))
            conn.commit()
            self.refresh_tree()
            self.admin_title.delete(0, tk.END)
            self.admin_author.delete(0, tk.END)
            self.admin_pdf_path.delete(0, tk.END)
            self.selected_id = None
            messagebox.showinfo("Deleted", "Book deleted.")

    def view_pdf(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a book to view PDF.")
            return
        pdf_path = self.admin_pdf_path.get() if hasattr(self, "admin_pdf_path") else self.user_pdf_path.get()
        if os.path.exists(pdf_path):
            try:
                if os.name == "nt":
                    os.startfile(pdf_path)
                elif os.name == "posix":
                    subprocess.call(("open" if sys.platform == "darwin" else "xdg-open", pdf_path))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showerror("Error", "PDF file not found.")


# Run App
root = tk.Tk()
app = BookApp(root)
root.mainloop() 
