import tkinter as tk
from tkinter import messagebox
from common.button import CustomButton


class LoginPage:
    def __init__(self, master, app_manager):
        self.master = master
        self.app_manager = app_manager
        self.config()
        self.view()

    def config(self):
        self.master.title("Đăng nhập")
        self.master.geometry("300x200")

    def view(self):
        # Label tiêu đề
        label = tk.Label(self.master, text="Đăng nhập", font=("Arial", 20))
        label.pack(pady=10)

        # Label username
        lib_user = tk.Label(self.master, text="Username:")
        lib_user.place(x=20, y=60)

        # Label password
        lib_pass = tk.Label(self.master, text="Password:")
        lib_pass.place(x=20, y=100)

        # Ô nhập username
        self.entry_username = tk.Entry(self.master)
        self.entry_username.place(x=90, y=60)

        # Ô nhập password
        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.place(x=90, y=100)

        # Nút tạo tài khoản
        btn = CustomButton(
            self.master,
            text="Tạo tài khoản",
            command=self.tao_tk,
            style_type="primary"
        )
        btn.place(x=40, y=140)

        # Nút đăng nhập
        btn = CustomButton(
            self.master,
            text="Đăng nhập",
            command=self.login,
            style_type="success"
        )
        btn.place(x=160, y=140)

    def tao_tk(self):
        print("Chuyển sang trang tạo tài khoản")
        self.app_manager.show_taotk_page()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            file = open("database/tk.csv", "r", encoding="utf-8")

            for line in file:
                tk_info = line.strip().split(",")

                if len(tk_info) >= 2:
                    if username == tk_info[0] and password == tk_info[1]:
                        messagebox.showinfo("Thông báo", "Đăng nhập thành công")
                        file.close()
                        self.app_manager.show_quanlytk_page()
                        return  # ⚠️ thêm dòng này

            file.close()
            messagebox.showerror("Thông báo", "Đăng nhập thất bại")

        except FileNotFoundError:
            messagebox.showerror("Thông báo", "Chưa có tài khoản nào được tạo")