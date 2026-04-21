import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Thêm thư viện này để xử lý ảnh PNG
import os


class DashboardPage:
    def __init__(self, master, app, username):
        self.master = master
        self.app = app
        self.username = username
        self.dropdown_visible = False

        # Màu sắc chủ đạo
        self.color_navy = "#1e376d"
        self.color_text = "#1e376d"

        # Đường dẫn ảnh (Lấy thư mục hiện tại -> vào folder images -> file logo.png)
        current_dir = os.path.dirname(__file__)
        self.logo_path = os.path.join(os.path.dirname(current_dir), "assets", "logo.png")

        self.build_ui()

    def build_ui(self):
        # 1. ===== BANNER TRẮNG =====
        banner_top = tk.Frame(self.master, bg="#f0fbff", height=120)
        banner_top.pack(fill="x")
        banner_top.pack_propagate(False)

        # --- PHẦN LOGO MỚI ---
        try:
            # Mở và chỉnh kích thước ảnh
            img = Image.open(self.logo_path)
            img = img.resize((120, 100), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)

            logo_label = tk.Label(banner_top, image=self.logo_img, bg="#f0fbff")
            logo_label.pack(side="left", padx=50, pady=10)
        except Exception as e:
            print(f"Lỗi load ảnh: {e}")

        # Cụm chữ tiêu đề trung tâm
        title_frame = tk.Frame(banner_top, bg="white")
        title_frame.pack(side="left", expand=True)

        tk.Label(
            title_frame,
            text="TRƯỜNG TIỂU HỌC QUANG TRUNG",
            fg=self.color_text,
            bg="#f0fbff",
            font=("Times New Roman", 26, "bold")
        ).pack()

        # 2. ===== THANH MENU =====
        nav_bar = tk.Frame(self.master, bg=self.color_navy, height=45)
        nav_bar.pack(fill="x")

        menu_items = [
            ("🏠 TRANG CHỦ", self.home),
            ("📚 QUẢN LÝ HS", self.students),
            ("💰 TÀI CHÍNH", self.taichinh),
            ("📊 ĐÁNH GIÁ", self.danhgia),
        ]

        for text, cmd in menu_items:
            btn = tk.Button(
                nav_bar, text=text, fg="white", bg=self.color_navy,
                activebackground="#2a4d9c", activeforeground="white",
                bd=0, font=("Arial", 10, "bold"), padx=15, cursor="hand2",
                command=cmd
            )
            btn.pack(side="left", fill="y")

        # Nút User
        self.user_label = tk.Label(
            nav_bar, text=f"👤 {self.username} ▼", fg="white",
            bg=self.color_navy, font=("Arial", 10, "bold"),
            cursor="hand2", padx=20
        )
        self.user_label.pack(side="right", fill="y")
        self.user_label.bind("<Button-1>", self.toggle_dropdown)

        # 3. ===== DROPDOWN MENU =====
        self.dropdown = tk.Frame(self.master, bg="white", bd=1, relief="solid")
        tk.Button(
            self.dropdown, text="Đăng xuất", bg="white",
            fg="black", bd=0, command=self.logout,
            activebackground="#f0f0f0", font=("Arial", 10)
        ).pack(fill="x", padx=10, pady=5)

        # 4. ===== VÙNG NỘI DUNG =====
        self.content = tk.Frame(self.master, bg="#f5f6fa")
        self.content.pack(fill="both", expand=True)

        self.home()

    # --- Các hàm bổ trợ giữ nguyên ---
    def toggle_dropdown(self, event):
        if self.dropdown_visible:
            self.dropdown.place_forget()
            self.dropdown_visible = False
        else:
            x = self.user_label.winfo_rootx() - self.master.winfo_rootx()
            y = 165
            self.dropdown.place(x=x, y=y, width=120)
            self.dropdown.lift()
            self.dropdown_visible = True

    def clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def home(self):
        self.clear()
        tk.Label(self.content, text="Chào mừng bạn đến với hệ thống!",
                 font=("Arial", 18), bg="#f5f6fa").pack(pady=50)

    def students(self):
        self.clear()
        tk.Label(self.content, text="Quản lý hồ sơ học sinh",
                 font=("Arial", 18), bg="#f5f6fa").pack(pady=50)

    def danhgia(self):
        self.clear()
        tk.Label(self.content, text="Bảng đánh giá kết quả",
                 font=("Arial", 18), bg="#f5f6fa").pack(pady=50)

    def taichinh(self):
        self.clear()
        tk.Label(self.content, text="Thông tin học phí & Tài chính",
                 font=("Arial", 18), bg="#f5f6fa").pack(pady=50)

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            self.app.show_login()