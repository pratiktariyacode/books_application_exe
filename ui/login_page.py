import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import os
import re
from ui import signup_page
from ui import user_dashboard
from ui import admin_panel


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
    conn = sqlite3.connect("users.db")
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

    # ✅ Load background image
    image_path = os.path.join("ui/book5.png")  # ✅ make sure this path is correct
    if os.path.exists(image_path):
        bg_image = Image.open(image_path).resize((width, height))
        bg_photo = ctk.CTkImage(light_image=bg_image, size=(width, height))
        root.bg_photo = bg_photo

        bg_label = ctk.CTkLabel(root, image=bg_photo, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ✅ Card Frame (Login Form Container)
    card_frame = ctk.CTkFrame(root, width=420, height=430, corner_radius=40, fg_color="black")
    card_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ✅ Title
    ctk.CTkLabel(card_frame, text="Login", text_color="white", font=("Arial", 32, "bold")).place(relx=0.5, rely=0.1, anchor="center")

    # ✅ Email Label and Entry
    ctk.CTkLabel(card_frame, text="Email:", text_color="white", font=("Arial", 16)).place(relx=0.15, rely=0.25, anchor="w")
    email_entry = ctk.CTkEntry(card_frame, placeholder_text="Enter your email", width=250, height=40)
    email_entry.place(relx=0.5, rely=0.35, anchor="center")

    # ✅ Password Label and Entry
    ctk.CTkLabel(card_frame, text="Password:", text_color="white", font=("Arial", 16)).place(relx=0.15, rely=0.47, anchor="w")
    password_entry = ctk.CTkEntry(card_frame, placeholder_text="Enter your password", show="*", width=250, height=40)
    password_entry.place(relx=0.5, rely=0.57, anchor="center")

    # ✅ Login Handler
    def handle_login():
        email = email_entry.get()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter all fields")
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if not re.match(email_pattern, email):
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

    # ✅ Buttons
    login_button = ctk.CTkButton(card_frame, text="Login", width=200, height=35, command=handle_login)
    login_button.place(relx=0.5, rely=0.72, anchor="center")

    signup_button = ctk.CTkButton(card_frame, text="Create New Account", command=open_signup, width=200, height=35)
    signup_button.place(relx=0.5, rely=0.84, anchor="center")

    root.maxsize(1000, 700)
    root.iconbitmap("ui/icon.ico")
    root.mainloop()


if __name__ == '__main__':
    main()  