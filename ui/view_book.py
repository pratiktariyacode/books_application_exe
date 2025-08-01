import customtkinter as ctk
from tkinter import messagebox, filedialog
import sqlite3
import os
import shutil
import webbrowser
import sys
from PIL import Image

# ✅ PyInstaller-compatible path resolver
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Paths
DB_PATH = resource_path("users.db")
BG_IMAGE_PATH = resource_path("ui/book1.jpg")
ICON_PATH = resource_path("ui/icon.ico")

def fetch_books():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, pdf_path, image_path FROM books")
        books = cursor.fetchall()
        conn.close()
        return books
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching books:\n{e}")
        return []

def delete_book_from_db(book_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error deleting book:\n{e}")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = ctk.CTkToplevel()
    root.title("View Books")
    width, height = 1000, 700
    center_window(root, width, height)
    root.resizable(False, False)

    # ✅ Set icon
    if os.path.exists(ICON_PATH):
        root.iconbitmap(ICON_PATH)

    # ✅ Background Image
    if os.path.exists(BG_IMAGE_PATH):
        bg_image = Image.open(BG_IMAGE_PATH).resize((width, height))
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(width, height))
        bg_label = ctk.CTkLabel(root, image=bg_ctk, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    container = ctk.CTkFrame(root, width=960, height=650, fg_color="white", corner_radius=20)
    container.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(container, text="Available Books", font=("Arial", 25, "bold"), text_color="black").pack(pady=(20, 5))

    top_row = ctk.CTkFrame(container, fg_color="transparent")
    top_row.pack(pady=5)

    search_var = ctk.StringVar()
    search_entry = ctk.CTkEntry(top_row, placeholder_text="Search by title...", textvariable=search_var,
                                 width=300, height=30, text_color="white")
    search_entry.pack(side="left", padx=5)

    def search_books():
        query = search_var.get().lower()
        refresh_books(query)

    ctk.CTkButton(top_row, text="Search", command=search_books).pack(side="left", padx=5)
    ctk.CTkButton(top_row, text="Refresh", command=lambda: refresh_books()).pack(side="left", padx=5)

    book_frame = ctk.CTkScrollableFrame(container, width=920, height=500, fg_color="transparent")
    book_frame.pack(pady=10)

    def refresh_books(query=None):
        for widget in book_frame.winfo_children():
            widget.destroy()
        show_books(query)

    def show_books(search_term=None):
        books = fetch_books()
        if search_term:
            books = [b for b in books if search_term in b[1].lower()]
        if not books:
            ctk.CTkLabel(book_frame, text="No books found.", font=("Arial", 18), text_color="black").pack(pady=20)
        else:
            for book_id, title, pdf_path, image_path in books:
                def open_pdf(p=pdf_path):
                    if os.path.isfile(p):
                        try:
                            webbrowser.open_new(os.path.abspath(p))
                        except Exception as e:
                            messagebox.showerror("Open Error", f"Could not open PDF:\n{e}")
                    else:
                        messagebox.showerror("File Not Found", f"The PDF file was not found:\n{p}")

                def download_pdf(p=pdf_path):
                    if os.path.isfile(p):
                        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                                 filetypes=[("PDF files", "*.pdf")])
                        if save_path:
                            try:
                                shutil.copy(p, save_path)
                                messagebox.showinfo("Download Complete", f"File saved to:\n{save_path}")
                            except Exception as e:
                                messagebox.showerror("Download Error", f"Could not save file:\n{e}")
                    else:
                        messagebox.showerror("File Not Found", f"The PDF file was not found:\n{p}")

                def delete_pdf(bid=book_id, p=pdf_path):
                    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this book and its PDF?")
                    if confirm:
                        try:
                            if os.path.isfile(p):
                                os.remove(p)
                            delete_book_from_db(bid)
                            messagebox.showinfo("Deleted", "Book and PDF deleted successfully.")
                            refresh_books()
                        except Exception as e:
                            messagebox.showerror("Delete Error", f"Could not delete:\n{e}")

                row = ctk.CTkFrame(book_frame, fg_color="transparent")
                row.pack(fill="x", pady=5, padx=10)

                if image_path and os.path.isfile(image_path):
                    try:
                        img = Image.open(image_path).resize((120, 80))
                        book_img = ctk.CTkImage(light_image=img, size=(120, 80))
                        ctk.CTkLabel(row, image=book_img, text="").pack(side="left", padx=10)
                    except Exception as e:
                        print(f"Image load error: {e}")
                else:
                    ctk.CTkLabel(row, text="No Image", width=120, height=80, text_color="gray").pack(side="left", padx=10)

                ctk.CTkLabel(row, text=title, font=("Arial", 16), anchor="w", text_color="black").pack(side="left", padx=10, fill="x", expand=True)
                ctk.CTkButton(row, text="Open PDF", command=open_pdf, width=90).pack(side="right", padx=3)
                ctk.CTkButton(row, text="Download", command=download_pdf, width=90).pack(side="right", padx=3)
                ctk.CTkButton(row, text="Delete", command=delete_pdf, fg_color="red", width=90).pack(side="right", padx=3)

    show_books()
    return root

if __name__ == "__main__":
    win = main()
    win.mainloop()
