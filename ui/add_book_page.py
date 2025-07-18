import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import os
import sqlite3
import sys

def resource_path(relative_path):
    """Get absolute path to resource (for dev and for PyInstaller)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Absolute paths using resource_path
IMAGE_DIR = resource_path("assets/images")
PDF_DIR = resource_path("assets/pdf")

def ensure_asset_folders():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_book_table():
    conn = sqlite3.connect(resource_path("users.db"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_path TEXT,
            pdf_path TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_book_to_db(title, image_path, pdf_path):
    conn = sqlite3.connect(resource_path("users.db"))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, image_path, pdf_path) VALUES (?, ?, ?)", (title, image_path, pdf_path))
    conn.commit()
    conn.close()

def main():
    ensure_asset_folders()
    create_book_table()

    root = ctk.CTk()
    root.title("Add Book")

    ctk.CTkLabel(root, text="Add New Book", font=("Arial", 30, "bold")).pack(pady=20)

    title_entry = ctk.CTkEntry(root, placeholder_text="Enter Book Title", width=400, height=40)
    title_entry.pack(pady=15)

    image_label = ctk.CTkLabel(root, text="No image selected")
    image_label.pack()

    pdf_label = ctk.CTkLabel(root, text="No PDF selected")
    pdf_label.pack()

    image_path = ""
    pdf_path = ""

    def browse_image():
        nonlocal image_path
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file:
            dest_path = os.path.join(IMAGE_DIR, os.path.basename(file))
            shutil.copy(file, dest_path)
            image_path = dest_path
            image_label.configure(text=f"Image: {os.path.basename(file)}")

    def browse_pdf():
        nonlocal pdf_path
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            dest_path = os.path.join(PDF_DIR, os.path.basename(file))
            shutil.copy(file, dest_path)
            pdf_path = dest_path
            pdf_label.configure(text=f"PDF: {os.path.basename(file)}")

    def add_book():
        title = title_entry.get().strip()
        if not title or not image_path or not pdf_path:
            messagebox.showerror("Error", "Please enter all fields and upload files.")
            return

        save_book_to_db(title, image_path, pdf_path)
        messagebox.showinfo("Success", "Book added successfully!")

        title_entry.delete(0, 'end')
        image_label.configure(text="No image selected")
        pdf_label.configure(text="No PDF selected")

    ctk.CTkButton(root, text="Upload Cover Image", command=browse_image).pack(pady=5)
    ctk.CTkButton(root, text="Upload PDF", command=browse_pdf).pack(pady=5)
    ctk.CTkButton(root, text="Add Book", command=add_book).pack(pady=20)

    center_window(root, 700, 500)
    root.mainloop()

if __name__ == "__main__":
    main()
