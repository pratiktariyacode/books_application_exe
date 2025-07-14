import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from ui import login_page  

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_user_table():
    conn = sqlite3.connect("users.db")
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
    conn = sqlite3.connect("users.db")
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

    ctk.CTkLabel(root, text="Sign Up", font=("Arial", 35, "bold")).pack(pady=40)

    username_entry = ctk.CTkEntry(root, placeholder_text="Username", width=250, height=40)
    username_entry.pack(pady=10)

    email_entry = ctk.CTkEntry(root, placeholder_text="Email", width=250, height=40)
    email_entry.pack(pady=10)

    password_entry = ctk.CTkEntry(root, placeholder_text="Password", show="*", width=250, height=40)
    password_entry.pack(pady=10)

    def handle_signup():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        if save_user(username, email, password):
            messagebox.showinfo("Success", "Account created! Please log in.")
            root.destroy()
            login_page.main()
        else:
            messagebox.showerror("Error", "Email already exists. Try another.")

    signup_button = ctk.CTkButton(root, text="Sign Up", width=200, height=35, command=handle_signup)
    signup_button.pack(pady=20)

    login_button = ctk.CTkButton(root, text="Already have an account? Login", command=open_login, width=200, height=35)
    login_button.pack()

    center_window(root, 900, 600)
    root.mainloop()
