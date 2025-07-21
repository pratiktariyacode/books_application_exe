import customtkinter as ctk
from ui import add_book_page
from ui import view_book
from ui import login_page
from PIL import Image
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ✅ Image paths
BG_IMAGE_PATH = resource_path("ui/book3.webp")
RIGHT_IMAGE_PATH = resource_path("ui/book_icon.png")

def open_view_book_page():
    if hasattr(open_view_book_page, "window") and open_view_book_page.window.winfo_exists():
        open_view_book_page.window.focus()
        return
    open_view_book_page.window = view_book.main()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def logout_fun():
    root.destroy()
    login_page.main()

# ✅ Prevent duplicate Add Book windows
def open_add_book_page():
    if hasattr(open_add_book_page, "window") and open_add_book_page.window.winfo_exists():
        open_add_book_page.window.focus()
        return
    open_add_book_page.window = add_book_page.main()


def main(user_email=None):
    global root
    root = ctk.CTk()
    root.title("User Dashboard")

    width, height = 1000, 700
    root.geometry(f"{width}x{height}")
    center_window(root, width, height)
    root.resizable(False, False)

    # ✅ Background image
    if os.path.exists(BG_IMAGE_PATH):
        bg_image = Image.open(BG_IMAGE_PATH).resize((width, height))
        bg_ctk_image = ctk.CTkImage(light_image=bg_image, size=(width, height))
        root.bg_ref = bg_ctk_image
        bg_label = ctk.CTkLabel(root, image=bg_ctk_image, text="")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # ✅ Left card container
    border_frame = ctk.CTkFrame(root, width=420, height=440, corner_radius=55, fg_color="black")
    border_frame.place(relx=0.25, rely=0.5, anchor="center")

    # ✅ Inner card
    card_frame = ctk.CTkFrame(border_frame, width=420, height=440, corner_radius=50, fg_color="white")
    card_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ✅ Welcome text
    ctk.CTkLabel(
        card_frame,
        text=f"Welcome, {user_email or 'User'}",
        font=("Arial", 26, "bold"),
        text_color="black"
    ).pack(pady=(30, 20))

    # ✅ Add Book Button (no duplicate windows)
    ctk.CTkButton(
        card_frame,
        text="➕ Add Book",
        width=220,
        height=45,
        corner_radius=25,
        font=("Arial", 14, "bold"),
        command=open_add_book_page
    ).pack(pady=10)

    # ✅ View Book Button (no duplicate windows)
    ctk.CTkButton(
        card_frame,
        text="📚 View My Books",
        width=220,
        height=45,
        corner_radius=25,
        font=("Arial", 14, "bold"),
        command=open_view_book_page
    ).pack(pady=10)

    # ✅ Logout Button
    ctk.CTkButton(
        card_frame,
        text="🚪 Logout",
        width=220,
        height=45,
        corner_radius=25,
        font=("Arial", 14, "bold"),
        fg_color="#ff4d4d",
        hover_color="#e60000",
        text_color="white",
        command=logout_fun
    ).pack(pady=(30, 10))

    # ✅ Right-side image
    if os.path.exists(RIGHT_IMAGE_PATH):
        side_image = Image.open(RIGHT_IMAGE_PATH).resize((350, 350))
        side_ctk_image = ctk.CTkImage(light_image=side_image, size=(350, 350))
        image_label = ctk.CTkLabel(root, image=side_ctk_image, text="")
        image_label.place(relx=0.9, rely=0.5, anchor="center")
    root.iconbitmap("ui/icon.ico")
    root.mainloop()

if __name__ == '__main__':
    main()
