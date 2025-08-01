import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import os
import sys

# ✅ Resource path for PyInstaller compatibility
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Centering the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x}+{y}")

# ✅ Get all users from database
def get_all_users():
    conn = sqlite3.connect(resource_path("users.db"))
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# ✅ Delete a user
def delete_user(user_id, refresh_callback):
    conn = sqlite3.connect(resource_path("users.db"))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", f"User with ID {user_id} has been deleted.")
    refresh_callback()

# ✅ Main function
def main():
    global root
    root = ctk.CTk()
    root.title("Admin Panel")

    ctk.CTkLabel(root, text="Admin Panel", font=("Arial", 35, "bold")).pack(pady=20)

    frame = ctk.CTkScrollableFrame(root, width=700, height=400)
    frame.pack(pady=10)

    def load_users():
        for widget in frame.winfo_children():
            widget.destroy()

        users = get_all_users()

        if not users:
            ctk.CTkLabel(frame, text="No users found.", font=("Arial", 16)).pack(pady=10)
            return

        for user in users:
            user_id, username, email = user
            user_frame = ctk.CTkFrame(frame)
            user_frame.pack(pady=5, fill='x', padx=10)

            ctk.CTkLabel(user_frame, text=f"ID: {user_id}", width=50).pack(side='left', padx=10)
            ctk.CTkLabel(user_frame, text=f"Username: {username}", width=200).pack(side='left', padx=10)
            ctk.CTkLabel(user_frame, text=f"Email: {email}", width=200).pack(side='left', padx=10)

            del_btn = ctk.CTkButton(user_frame, text="Delete", width=80, fg_color="red",
                                     command=lambda uid=user_id: delete_user(uid, load_users))
            del_btn.pack(side='right', padx=10)

    load_users()

    center_window(root, 900, 600)

    # ✅ Optional: Set icon if needed
    icon_path = resource_path("ui/icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    root.mainloop()

if __name__ == '__main__':
    main()
