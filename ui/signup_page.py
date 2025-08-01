import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os
import re
import sys
from ui import login_page

# ✅ PyInstaller-compatible path fetcher
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_user_table():
    db_path = resource_path("users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_user(username, email, password):
    db_path = resource_path("users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def open_login():
    root.destroy()
    login_page.main()

def main():
    global root
    create_user_table()

    root = ctk.CTk()
    root.title("Book Store - Sign Up")
    root.configure(fg_color="white")

    width, height = 1000, 700
    center_window(root, width, height)

    # ✅ Background Image (with resource_path)
    image_path = resource_path("ui/book5.png")
    if os.path.exists(image_path):
        bg_image = Image.open(image_path).resize((width, height))
        bg_photo = ctk.CTkImage(light_image=bg_image, size=(width, height))
        root.bg_photo = bg_photo
        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ✅ Card Frame
    card_frame = ctk.CTkFrame(root, width=460, height=500, corner_radius=40, fg_color="black")
    card_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card_frame, text="Sign Up", text_color="white", font=("Arial", 32, "bold")).place(relx=0.5, rely=0.1, anchor="center")
    ctk.CTkLabel(card_frame, text="Username:", text_color="white", font=("Arial", 16)).place(relx=0.5, rely=0.19, anchor="center")
    username_entry = ctk.CTkEntry(card_frame, placeholder_text="Username", width=250, height=40)
    username_entry.place(relx=0.5, rely=0.25, anchor="center")

    ctk.CTkLabel(card_frame, text="Email:", text_color="white", font=("Arial", 16)).place(relx=0.5, rely=0.32, anchor="center")
    email_entry = ctk.CTkEntry(card_frame, placeholder_text="Email", width=250, height=40)
    email_entry.place(relx=0.5, rely=0.38, anchor="center")

    ctk.CTkLabel(card_frame, text="Password:", text_color="white", font=("Arial", 16)).place(relx=0.5, rely=0.45, anchor="center")
    password_entry = ctk.CTkEntry(card_frame, placeholder_text="Password", show="*", width=250, height=40)
    password_entry.place(relx=0.5, rely=0.51, anchor="center")

    def handle_signup():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if save_user(username, email, password):
            messagebox.showinfo("Success", "Account created! Please log in.")
            root.destroy()
            login_page.main()
        else:
            messagebox.showerror("Error", "Email already exists. Try another.")

    signup_button = ctk.CTkButton(card_frame, text="Sign Up", width=200, height=35, command=handle_signup)
    signup_button.place(relx=0.5, rely=0.65, anchor="center")

    login_button = ctk.CTkButton(card_frame, text="Already have an account? Login", command=open_login, width=200, height=35)
    login_button.place(relx=0.5, rely=0.77, anchor="center")

    # ✅ App Icon
    icon_path = resource_path("ui/icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    root.maxsize(1000, 700)
    root.mainloop()

if __name__ == '__main__':
    main()
