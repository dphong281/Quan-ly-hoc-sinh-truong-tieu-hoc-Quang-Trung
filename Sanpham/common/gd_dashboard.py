import tkinter as tk
from PIL import Image, ImageTk


class DashboardPage:
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager
        self.username = username

        # khung
        self.master.configure(bg="#F7FAFC")

        # Gọi các hàm con để xây dựng giao diện
        self.gd_sidebar()  # Đổi tên hàm để tránh trùng tên với biến self.sidebar
        self.main_content()
        self.mc_header()

    def gd_sidebar(self):
        """Thiết kế phần Sidebar bên trái (Màu xanh) với hiệu ứng"""
        self.sidebar = tk.Frame(self.master, bg="#0d62b8", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        img_side = Image.open("assets/logo.png")
        img_side = img_side.resize((190, 120), Image.LANCZOS)
        self.photo_side = ImageTk.PhotoImage(img_side)

        self.lbl_logo_side = tk.Label(self.sidebar, image=self.photo_side, bg="#0d62b8")
        self.lbl_logo_side.pack(pady=25)

        # Danh sách các nút menu
        menu_items = ["Dashboard", "Học Sinh", "Giáo Viên", "Lớp Học", "Lịch Học", "Cài Đặt"]

        for item in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {item}",
                fg="white",
                bg="#0d62b8",
                font=("Arial", 12, "bold"),
                bd=0,
                anchor="w",
                cursor="hand2",
                activebackground="#0a4d91",  # Màu khi nhấn giữ
                activeforeground="white"
            )
            btn.pack(fill="x", pady=2, padx=10, ipady=8)

            # Hiệu ứng di chuột (Hover) cho Menu
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1a73e8"))  # Xanh sáng hơn khi di vào
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#0d62b8"))  # Về màu cũ khi rời đi

        # Nút Đăng xuất
        self.btn_logout = tk.Button(
            self.sidebar,
            text=" 🚪 Đăng xuất",
            fg="#FEB2B2",  # Màu hồng nhạt cho chữ
            bg="#0d62b8",
            font=("Arial", 11, "bold"),
            bd=0,
            anchor="w",
            cursor="hand2",
            command=lambda: self.app_manager.show_login()
        )
        self.btn_logout.pack(side="bottom", fill="x", pady=20, padx=10, ipady=8)

        # Hiệu ứng Hover riêng cho nút Đăng xuất (Chuyển sang đỏ)
        self.btn_logout.bind("<Enter>", lambda e: self.btn_logout.config(bg="#e53e3e", fg="white"))
        self.btn_logout.bind("<Leave>", lambda e: self.btn_logout.config(bg="#0d62b8", fg="#FEB2B2"))

    def main_content(self):
        """Thiết kế khung nội dung chính bên phải (Màu trắng)"""
        self.main_area = tk.Frame(self.master, bg="#F7FAFC")
        self.main_area.pack(side="right", fill="both", expand=True)

    def mc_header(self):
        """Thiết kế thanh Header với đường kẻ bóng nhẹ"""
        self.header = tk.Frame(self.main_area, bg="white", height=60)  # Tăng chiều cao header cho thoáng
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Đường kẻ mỏng tạo hiệu ứng tách biệt (Shadow nhẹ)
        line = tk.Frame(self.main_area, bg="#E2E8F0", height=1)
        line.pack(fill="x")

        # Lời chào người dùng
        tk.Label(
            self.header, text=f"Xin chào, {self.username} ",
            bg="white", fg="#2D3748", font=("Arial", 12, "bold")
        ).pack(side="left", padx=30)
