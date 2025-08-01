import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os
import re
import sys
from ui import signup_page, user_dashboard, admin_panel

# ✅ For PyInstaller: handle correct path for images/db/icons
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # When bundled by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_signup():
    root.destroy()
    signup_page.main()

def login_user(email, password):
    db_path = resource_path("users.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def main():
    global root
    root = ctk.CTk()
    root.title("Book Store - Login")
    width, height = 1000, 700
    center_window(root, width, height)
    root.configure(fg_color="white")

    # ✅ Background image path fix
    image_path = resource_path("ui/book5.png")
    if os.path.exists(image_path):
        bg_image = Image.open(image_path).resize((width, height))
        bg_photo = ctk.CTkImage(light_image=bg_image, size=(width, height))
        root.bg_photo = bg_photo

        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ✅ Login Card
    card_frame = ctk.CTkFrame(root, width=420, height=430, corner_radius=40, fg_color="black")
    card_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card_frame, text="Login", text_color="white", font=("Arial", 32, "bold")).place(relx=0.5, rely=0.1, anchor="center")
    ctk.CTkLabel(card_frame, text="Email:", text_color="white", font=("Arial", 16)).place(relx=0.15, rely=0.25, anchor="w")

    email_entry = ctk.CTkEntry(card_frame, placeholder_text="Enter your email", width=250, height=40)
    email_entry.place(relx=0.5, rely=0.35, anchor="center")

    ctk.CTkLabel(card_frame, text="Password:", text_color="white", font=("Arial", 16)).place(relx=0.15, rely=0.47, anchor="w")
    password_entry = ctk.CTkEntry(card_frame, placeholder_text="Enter your password", show="*", width=250, height=40)
    password_entry.place(relx=0.5, rely=0.57, anchor="center")

    def handle_login():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        user = login_user(email, password)

        if user:
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
            user_dashboard.main(user_email=email)
        elif email == "admin@gmail.com" and password == "admin":
            email_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            root.destroy()
            admin_panel.main()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    login_button = ctk.CTkButton(card_frame, text="Login", width=200, height=35, command=handle_login)
    login_button.place(relx=0.5, rely=0.72, anchor="center")

    signup_button = ctk.CTkButton(card_frame, text="Create New Account", command=open_signup, width=200, height=35)
    signup_button.place(relx=0.5, rely=0.84, anchor="center")

    # ✅ Icon fix with resource path
    icon_path = resource_path("ui/icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    root.maxsize(1000, 700)
    root.mainloop()

if __name__ == '__main__':
    main()
