import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class LoginPage:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        # --- MÀU SẮC ---
        self.bg_color = "#cfebff"
        self.card_color = "white"
        self.btn_color = "#5bc0de"

        current_dir = os.path.dirname(__file__)
        self.logo_path = os.path.join(os.path.dirname(current_dir), "assets", "logo.png")

        self.view()

    def view(self):
        self.master.configure(bg=self.bg_color)

        # --- KHUNG ĐĂNG NHẬP ---
        self.card = tk.Frame(self.master, bg=self.card_color, padx=40, pady=30,
                             highlightthickness=1, highlightbackground="#dcdcdc")
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # LOGO
        try:
            img = Image.open(self.logo_path)
            img = img.resize((150, 110), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.card, image=self.logo_img, bg=self.card_color).pack(pady=(0, 10))
        except:
            tk.Label(self.card, text="[ LOGO TRƯỜNG ]", bg=self.card_color, fg="gray").pack()

        # TIÊU ĐỀ
        tk.Label(self.card, text="Đăng nhập", font=("Arial", 20),
                 bg=self.card_color, fg="#333").pack(pady=(0, 20))


        # USERNAME
        self.entry_user = self.create_input_row("👤", "")
        # FIX: Bind phím Enter cho ô Username
        self.entry_user.bind('<Return>', self.login)

        # PASSWORD
        self.entry_pass = self.create_input_row("🔒", "", is_password=True)
        # FIX: Bind phím Enter cho ô Password
        self.entry_pass.bind('<Return>', self.login)

        # NÚT ĐĂNG NHẬP
        btn_login = tk.Button(self.card, text="➜ Đăng nhập", bg=self.btn_color, fg="white",
                              font=("Arial", 11, "bold"), bd=0, cursor="hand2",
                              command=self.login)
        btn_login.pack(fill="x", pady=(20, 10), ipady=8)

        self.master.bind('<Return>', self.login)

        self.entry_user.focus_set()

    def create_input_row(self, icon_text, default_val, is_password=False, is_readonly=False):
        row = tk.Frame(self.card, bg=self.card_color)
        row.pack(fill="x", pady=5)

        # Label icon
        tk.Label(row, text=icon_text, bg="#f5f5f5", width=4,
                 relief="solid", bd=1, font=("Arial", 12)).pack(side="left", fill="y")

        entry = tk.Entry(row, font=("Arial", 11), relief="solid", bd=1)
        if default_val:
            entry.insert(0, default_val)
        if is_password:
            entry.config(show="*")
        if is_readonly:
            entry.config(state="readonly", readonlybackground="white")

        entry.pack(side="left", fill="x", expand=True, ipady=6)
        return entry

    def login(self, event=None):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        if not u or not p:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ Username và Password")
            return

        # Đường dẫn tk.csv
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "database", "tk.csv")

        try:
            if not os.path.exists(file_path):
                messagebox.showerror("Lỗi", f"Không tìm thấy file tài khoản tại:\n{file_path}")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 2:
                        if u == data[0] and p == data[1]:
                            self.master.unbind('<Return>')
                            messagebox.showinfo("Thành công", "Đăng nhập hệ thống thành công!")
                            self.app.show_dashboard(u)
                            return

            messagebox.showerror("Thất bại", "Tài khoản hoặc mật khẩu không đúng")

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", str(e))