import tkinter as tk
import Sanpham.page.login as LoginLogic
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

class LoginPage:
    def __init__(self, master, app_maneger):
        self.master = master
        self.app_maneger = app_maneger
        self.config()
        self.view()

    def config(self):
        self.master.configure(background="#D1E9F6")

    def view(self):
        #khung
        self.frame_login = tk.Frame(
            self.master, bg="white", width=400, height=600,
            highlightbackground="#CCCCCC", highlightthickness=1, bd=0
        )
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_login.pack_propagate(False)

        # Logo
        img = Image.open("assets/logo.png")
        img = img.resize((200, 130), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.lbl_logo = tk.Label(self.frame_login, image=self.photo, bg="white")
        self.lbl_logo.pack(pady=(20, 0))

        #Tiêu đề
        self.lbl_title = tk.Label(
            self.frame_login,
            text="ĐĂNG NHẬP", bg="white", fg="#333333", font=("Arial", 22, "bold")
        )
        self.lbl_title.pack(pady=(10, 20))

        # Username
        tk.Label(self.frame_login, text="Username", bg="white", fg="#666666", font=("Arial", 10)).pack(fill="x", padx=40)
        self.entry_user = tk.Entry(
            self.frame_login, bg="#F0F0F0", font=("Arial", 12),
            bd=0, highlightthickness=1, highlightbackground="#E0E0E0"
        )
        self.entry_user.pack(fill="x", padx=40, pady=(5, 15), ipady=5)

        # Password
        tk.Label(self.frame_login, text="Password", bg="white", fg="#666666", font=("Arial", 10)).pack(fill="x", padx=40)
        self.entry_pass = tk.Entry(
            self.frame_login, bg="#F0F0F0", font=("Arial", 13),
            bd=0, show="*", highlightthickness=1, highlightbackground="#E0E0E0"
        )
        self.entry_pass.pack(fill="x", padx=40, pady=(5, 30), ipady=5)

        #nut login
        self.btn_login = tk.Button(
            self.frame_login, text="Đăng nhập", font=("Arial", 12, "bold"),
            bg="#65C1D9", fg="white", bd=0, cursor="hand2",
            command=self.l_login
        )
        self.btn_login.pack(fill="x", padx=40, ipady=10)

        #hiệu ứng nút login
        self.btn_login.bind("<Enter>", self.on_enter)
        self.btn_login.bind("<Leave>", self.on_leave)

        #nut enter
        self.entry_user.bind("<Return>", self.handle_enter)
        self.entry_pass.bind("<Return>", self.handle_enter)

    def handle_enter(self, event):
        self.l_login()

    # hiệu ứng khi di chuột vào nút
    def on_enter(self, e):
        self.btn_login.config(bg="#52A9C1")

    # hiệu ứng khi di chuột ra khỏi nút
    def on_leave(self, e):
        self.btn_login.config(bg="#65C1D9")

    def l_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        if not u or not p:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        LoginLogic.kiem_tra_dang_nhap(u, p, self.app_maneger)