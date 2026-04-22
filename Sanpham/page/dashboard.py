import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

from Sanpham.page.trangchu import TrangChuView
from Sanpham.page.qlhs import QLHSView


class DashboardPage:
    def __init__(self, master, app, username):
        self.master = master
        self.app = app
        self.username = username
        self.dropdown_visible = False

        self.color_navy = "#1e376d"
        self.color_text = "#1e376d"

        current_dir = os.path.dirname(__file__)
        self.logo_path = os.path.join(os.path.dirname(current_dir), "assets", "logo.png")

        self.build_ui()

    def build_ui(self):
        # ===== BANNER =====
        self.banner_top = tk.Frame(self.master, bg="#f0fbff", height=120)
        self.banner_top.pack(fill="x")
        self.banner_top.pack_propagate(False)

        try:
            img = Image.open(self.logo_path)
            img = img.resize((130, 100), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)

            logo_label = tk.Label(self.banner_top, image=self.logo_img, bg="#f0fbff")
            logo_label.pack(side="left", padx=50, pady=10)
        except Exception as e:
            print(f"Lỗi load ảnh: {e}")

        title_frame = tk.Frame(self.banner_top, bg="#f0fbff")
        title_frame.pack(side="left", expand=True)

        tk.Label(
            title_frame,
            text="TRƯỜNG TIỂU HỌC QUANG TRUNG",
            fg=self.color_text,
            bg="#f0fbff",
            font=("Times New Roman", 26, "bold")
        ).pack()

        # ===== THANH MENU =====
        self.nav_bar = tk.Frame(self.master, bg=self.color_navy, height=45)
        self.nav_bar.pack(fill="x")

        menu_items = [
            (" TRANG CHỦ", self.home),
            (" QUẢN LÝ HS", self.students),
            (" TÀI CHÍNH", self.taichinh),
            (" ĐÁNH GIÁ", self.danhgia),
        ]

        for text, cmd in menu_items:
            btn = tk.Button(
                self.nav_bar, text=text, fg="white", bg=self.color_navy,
                activebackground="#2a4d9c", activeforeground="white",
                bd=0, font=("Arial", 10, "bold"), padx=15, cursor="hand2",
                command=cmd
            )
            btn.pack(side="left", fill="y")

        self.user_label = tk.Label(
            self.nav_bar, text=f"👤 {self.username} ▼", fg="white",
            bg=self.color_navy, font=("Arial", 10, "bold"),
            cursor="hand2", padx=20
        )
        self.user_label.pack(side="right", fill="y")
        self.user_label.bind("<Button-1>", self.toggle_dropdown)

        # ===== 3. THANH CHỮ CHẠY (Thêm self.) =====
        self.marquee_frame = tk.Frame(self.master, bg="#2a4d9c", height=30)
        self.marquee_frame.pack(fill="x")
        self.marquee_frame.pack_propagate(False)

        marquee_msg = "Chào mừng đến với hệ thống quản lý thông tin của trường Tiểu học Quang Trung - Chúc các thầy cô một ngày làm việc hiệu quả!"
        self.label_marquee = tk.Label(
            self.marquee_frame,
            text=marquee_msg,
            fg="white",
            bg="#2a4d9c",
            font=("Arial", 10, "italic bold")
        )

        self.marquee_x = 1000
        self.label_marquee.place(x=self.marquee_x, y=4)
        self.scroll_text()

        # ===== DROPDOWN MENU =====
        self.dropdown = tk.Frame(self.master, bg="white", bd=1, relief="solid")
        tk.Button(
            self.dropdown, text="Đăng xuất", bg="white",
            fg="black", bd=0, command=self.logout,
            activebackground="#f0f0f0", font=("Arial", 10)
        ).pack(fill="x", padx=10, pady=5)

        # ===== VÙNG NỘI DUNG =====
        self.content = tk.Frame(self.master, bg="#f5f6fa")
        self.content.pack(fill="both", expand=True)

        self.home()

    def scroll_text(self):
        self.marquee_x -= 2
        if self.marquee_x < -900:
            self.marquee_x = self.master.winfo_width()
        self.label_marquee.place(x=self.marquee_x, y=4)
        self.master.after(30, self.scroll_text)

    def toggle_dropdown(self, event):
        if self.dropdown_visible:
            self.dropdown.place_forget()
            self.dropdown_visible = False
        else:
            x = self.user_label.winfo_rootx() - self.master.winfo_rootx()

            if self.banner_top.winfo_viewable():
                y = 165
            else:
                y = 45

            self.dropdown.place(x=x, y=y, width=120)
            self.dropdown.lift()
            self.dropdown_visible = True

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def home(self):
        self.banner_top.pack(side="top", fill="x", before=self.nav_bar)
        self.marquee_frame.pack(fill="x", after=self.nav_bar)
        self.clear()
        try:
            TrangChuView(self.content)
        except Exception as e:
            tk.Label(self.content, text=f"Lỗi tải trang chủ: {e}", fg="red").pack(pady=20)

    def students(self):
        self.banner_top.pack_forget()
        self.marquee_frame.pack_forget()
        self.clear()
        QLHSView(self.content)

    def danhgia(self):
        self.clear()
        tk.Label(self.content, text=" BẢNG ĐÁNH GIÁ KẾT QUẢ",
                 font=("Arial", 18, "bold"), bg="#f5f6fa", fg=self.color_navy).pack(pady=50)

    def taichinh(self):
        self.clear()
        tk.Label(self.content, text=" THÔNG TIN HỌC PHÍ & TÀI CHÍNH",
                 font=("Arial", 18, "bold"), bg="#f5f6fa", fg=self.color_navy).pack(pady=50)

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            self.app.show_login()