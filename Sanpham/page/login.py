import tkinter as tk
from tkinter import messagebox
import os


class LoginPage:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.view()

    def view(self):
        # Header
        tk.Label(self.master, text="Đăng nhập", font=("Arial", 20)).pack(pady=20)

        # Username
        tk.Label(self.master, text="Username").pack()
        self.entry_user = tk.Entry(self.master)
        self.entry_user.pack()

        # Password
        tk.Label(self.master, text="Password").pack()
        self.entry_pass = tk.Entry(self.master, show="*")
        self.entry_pass.pack()

        self.entry_user.bind('<Return>', self.login)
        self.entry_pass.bind('<Return>', self.login)
        # Bind thêm vào cả cửa sổ chính cho chắc
        self.master.bind('<Return>', self.login)

        # Nút Login
        tk.Button(self.master, text="Login", command=self.login).pack(pady=10)

    def login(self, event=None):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        if not u or not p:
            messagebox.showerror("Lỗi", "Thiếu thông tin")
            return

        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "database", "tk.csv")

        try:
            if not os.path.exists(file_path):
                messagebox.showerror("Lỗi", f"Không tìm thấy file tại: {file_path}")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")

                    if len(data) >= 2:
                        if u == data[0] and p == data[1]:
                            self.master.unbind('<Return>')

                            messagebox.showinfo("OK", "Đăng nhập thành công")
                            self.app.show_dashboard(u)
                            return

            messagebox.showerror("Sai", "Sai tài khoản hoặc mật khẩu")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", str(e))