import tkinter as tk
from PIL import Image, ImageTk
from openpyxl.styles.builtins import title


class DashboardPage:
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager
        self.username = username

        # khung
        self.master.configure(bg="white")

        # Gọi các hàm con để xây dựng giao diện
        self.gd_sidebar()  # Đổi tên hàm để tránh trùng tên với biến self.sidebar
        self.gd_main_content()
        self.mc_header()
        self.mc_body()
        self.the_thong_ke()
        self.the_bieu_do()

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

    def gd_main_content(self):
        """Thiết kế khung nội dung chính bên phải (Màu trắng)"""
        self.main_area = tk.Frame(self.master, bg="#ebebeb")
        self.main_area.pack(side="right", fill="both", expand=True)

    def mc_header(self):
        """Thiết kế thanh Header chuyên nghiệp cho Main Content"""
        # 1. Khung Header chính (Màu trắng, có độ cao cố định)
        self.header = tk.Frame(self.main_area, bg="white", height=35)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # --- PHẦN BÊN TRÁI: Lời chào ---
        left_header = tk.Frame(self.header, bg="white")
        left_header.pack(side="left", padx=20, fill="y")

        tk.Label(
            left_header, text=f"Xin chào, {self.username} ! ",
            bg="white", fg="#2D3748", font=("Arial", 11, "bold")
        ).pack(side="left")

        # --- PHẦN BÊN PHẢI: Icon và Thông tin phụ ---
        right_header = tk.Frame(
            self.header,
            bg="white"
        )
        right_header.pack(
            side="right",
            padx=20,
            fill="y"
        )

        # Nút cài đặt nhanh hoặc hồ sơ
        btn_profile = tk.Button(
            right_header,
            text="👤 Profile",
            bg="white",
            fg="#4A5568",
            font=("Arial", 9, "bold"),
            bd=0,
            padx=15, pady=5,
            cursor="hand2",
            activebackground="#E2E8F0"
        )
        btn_profile.pack(side="left", padx=5)

    def mc_body(self):
        # 1. Khung chứa chính phải có expand=True và fill="both"
        self.noidung = tk.Frame(self.main_area, bg="#ebebeb")
        self.noidung.pack(fill="both", expand=True, padx=30, pady=20)

        # 2. Quan trọng: Cấp trọng số cho các cột của self.noidung
        self.noidung.columnconfigure(0, weight=7)  # Cột trái lấy 7 phần diện tích thừa
        self.noidung.columnconfigure(1, weight=3)  # Cột phải lấy 3 phần diện tích thừa
        self.noidung.rowconfigure(0, weight=1)  # Hàng này sẽ giãn hết chiều cao

        # 3. Thêm sticky="nsew" để các Frame này giãn ra theo ô Grid
        self.phan_trai = tk.Frame(self.noidung,
                                  bg="#ebebeb")
        self.phan_trai.grid(row=0,
                            column=0,
                            sticky="nsew",
                            padx=(0, 20)
                            )

        self.phan_phai = tk.Frame(self.noidung,
                                  bg="white",
                                  highlightthickness=1,
                                  highlightbackground="#E2E8F0")
        self.phan_phai.grid(row=0,
                            column=1,
                            sticky="nsew")

    def the_thong_ke(self):
        self.the_1 = tk.Frame(self.phan_trai, bg="#ebebeb")
        self.the_1.pack(fill="x", pady=(0, 20))

        # Chia 3 cột đều nhau cho 3 thẻ (mỗi cột weight=1)
        self.the_1.columnconfigure((0, 1, 2), weight=1)

        data = [
            ("Tổng học sinh", "1,500", "#4C51BF"),
            ("Học sinh mới", "25", "#48BB78"),
            ("Tổng giáo viên", "85", "#ECC94B")
        ]

        for i, (title, value, color) in enumerate(data):
            card = tk.Frame(
                self.the_1,
                bg="white",
                highlightthickness=1,
                highlightbackground="#E2E8F0"
            )
            # Dùng grid và sticky="nsew" để thẻ rộng ra theo cột
            card.grid(row=0, column=i, sticky="nsew", padx=(0, 15))

            # cố định kích thước
            card.config(height=100)
            card.grid_propagate(False)

            tk.Label(card, text=title, bg="white", fg="#718096", font=("Arial", 9, "bold")).pack(anchor="w", padx=15,
                                                                                                 pady=(15, 0))
            tk.Label(card, text=value, bg="white", fg="#2D3748", font=("Arial", 18, "bold")).pack(anchor="w", padx=15)
            tk.Frame(card, bg=color, height=4).pack(side="bottom", fill="x")

    def the_bieu_do(self):
        self.the_2 = tk.Frame(self.phan_trai, bg="#ebebeb")
        self.the_2.pack(fill="x", pady=(0, 20))

        self.the_2.columnconfigure((0, 1), weight=2)

        data = [
            ("s", "#4C51BF"),
            ("Học sinh mới", "#48BB78"),
        ]

        for i, (title, color) in enumerate(data):
            card_1 = tk.Frame(
                self.the_2,
                bg="white",
                highlightthickness=1,
                highlightbackground="#E2E8F0"
            )
            card_1.grid(row=0, column=i, sticky="nsew", padx=(0, 15))

            card_1.config(height=100)
            card_1.grid_propagate(False)

















