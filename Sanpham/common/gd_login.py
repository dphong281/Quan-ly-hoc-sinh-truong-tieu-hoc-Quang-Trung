import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
from Sanpham.page.login import LoginLogic


class LoginView:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.config()
        self.view()

    def config(self):
        self.master.configure(fg_color="#D1E9F6")

    def view(self):

        self.frame_login = ctk.CTkFrame(
            self.master, fg_color="white", width=400, height=500,
            corner_radius=15, border_width=1, border_color="#CCCCCC"
        )

        self.frame_login.grid(row=0, column=0)


        self.frame_login.grid_columnconfigure(0, weight=1)

        # LOGO
        img = Image.open("assets/logo.png")
        self.photo = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 130))
        self.lbl_logo = ctk.CTkLabel(self.frame_login, image=self.photo, text="")
        self.lbl_logo.pack(pady=(30, 10))

        self.lbl_title = ctk.CTkLabel(
            self.frame_login, text="ĐĂNG NHẬP",
            text_color="#333333", font=("Arial", 22, "bold")
        )
        self.lbl_title.pack(pady=(10, 20))

        # USERNAME
        ctk.CTkLabel(self.frame_login, text="Username", text_color="black", font=("Arial", 12)).pack(fill="x", padx=40)
        self.entry_user = ctk.CTkEntry(
            self.frame_login, fg_color="#F0F0F0", font=("Arial", 13),
            border_width=1, border_color="#E0E0E0"
        )
        self.entry_user.pack(fill="x", padx=40, pady=(5, 15))

        # PASSWORD
        ctk.CTkLabel(self.frame_login, text="Password", text_color="black", font=("Arial", 12)).pack(fill="x", padx=40)
        self.entry_pass = ctk.CTkEntry(
            self.frame_login, fg_color="#F0F0F0", font=("Arial", 13),
            border_width=1, border_color="#E0E0E0", show="*"
        )
        self.entry_pass.pack(fill="x", padx=40, pady=5)

        # NÚT
        self.btn_login = ctk.CTkButton(
            self.frame_login, text="Đăng nhập", font=("Arial", 13, "bold"),
            fg_color="#65C1D9", hover_color="#52A9C1",
            text_color="white", cursor="hand2",
            command=self.l_login
        )
        self.btn_login.pack(pady = 20, ipady=5)

    def l_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        if not u or not p:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        LoginLogic.kiem_tra_dang_nhap(u, p, self.app_manager)