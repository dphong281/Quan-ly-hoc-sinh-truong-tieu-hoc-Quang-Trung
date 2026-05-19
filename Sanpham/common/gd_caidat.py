import tkinter as tk
from textwrap import fill
from tkinter import ttk


class CaiDatView:
    def __init__(self, master, username):
        self.master = master
        self.username = username

        # Cấu hình màu nền cho vùng chứa chính
        self.master.configure(bg="#f8fafc")

        self.header()
        self.than_giao_dien()
        self.menu_trai()
        self.noi_dung_phai()

    def header(self):
        # --- 1. TIÊU ĐỀ TRANG CÀI ĐẶT ---
        header_frame = tk.Frame(self.master, bg="#3cb3de", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame, text="CÀI ĐẶT",
            font=("Arial", 14, "bold"), fg="white", bg="#3cb3de"
        ).pack(side="left", padx=20, pady=12)

    def than_giao_dien(self):
        # --- 2. KHUNG THÂN CHÍNH ---
        self.body_frame = tk.Frame(self.master, bg="#f8fafc")
        self.body_frame.pack(fill="both", expand=True, padx=15, pady=15)

    def menu_trai(self):
        # --- 3. MENU SIDEBAR BÊN TRÁI ---
        self.left_menu = tk.Frame(self.body_frame, bg="white", width=200, highlightthickness=1,
                                  highlightbackground="#e2e8f0")
        self.left_menu.pack(side="left", fill="y", padx=(0, 15))
        self.left_menu.pack_propagate(False)

        # Lưu các nút vào từ điển (dictionary) để file logic dễ gọi gán sự kiện
        self.menu_buttons = {}

        self.menu_buttons["Hệ thống"] = tk.Button(
            self.left_menu, text="⚙️ Hệ thống chung", font=("Arial", 10, "bold"),
            bg="#e2e8f0", fg="#2c3e50", bd=0, anchor="w", padx=15, pady=12, cursor="hand2"
        )
        self.menu_buttons["Hệ thống"].pack(fill="x")

        self.menu_buttons["Bảo mật"] = tk.Button(
            self.left_menu, text="🔒 Bảo mật", font=("Arial", 10),
            bg="white", fg="#4a5568", bd=0, anchor="w", padx=15, pady=12, cursor="hand2"
        )
        self.menu_buttons["Bảo mật"].pack(fill="x")


    def noi_dung_phai(self):

        self.right_content = tk.Frame(self.body_frame, bg="white", highlightthickness=1, highlightbackground="#e2e8f0")
        self.right_content.pack(side="left", fill="both", expand=True)

        # === 1. THÊM MỚI: Tạo 2 khung chứa chờ sẵn ở đây ===
        self.khung_he_thong = tk.Frame(self.right_content, bg="white")
        self.khung_bao_mat = tk.Frame(self.right_content, bg="white")

        self.khung_he_thong.pack(fill="both", expand=True)


        # khung he thong
        tk.Label(
            self.khung_he_thong, text="[ THÔNG TIN TÀI KHOẢN ]",
            font=("Arial", 10, "bold"), fg="#3cb3de", bg="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        tk.Frame(self.khung_he_thong, bg="#e2e8f0", height=1).pack(fill="x", padx=20, pady=(0, 10))


        row_user = tk.Frame(self.khung_he_thong, bg="white")
        row_user.pack(fill="x", padx=20, pady=3)
        tk.Label(row_user, text="Tên đăng nhập:", font=("Arial", 10), bg="white", width=16, anchor="w").pack(
            side="left")

        # Sử dụng Label thay vì Entry để không cho chỉnh sửa, hiển thị chính xác self.username
        self.lbl_username = tk.Label(row_user, text=self.username, font=("Arial", 10, "bold"), fg="#1a73e8", bg="white")
        self.lbl_username.pack(side="left")

        # Ô nhập Họ và Tên
        row_hoten = tk.Frame(self.khung_he_thong, bg="white")
        row_hoten.pack(fill="x", padx=20, pady=3)
        tk.Label(row_hoten, text="Họ và Tên:", font=("Arial", 10), bg="white", width=16, anchor="w").pack(side="left")
        self.ent_ho_ten = tk.Entry(row_hoten, font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1",
                                   bd=0)
        self.ent_ho_ten.insert(0, "")
        self.ent_ho_ten.pack(side="left", fill="x", expand=True, ipady=3)

        # Ô nhập Email
        row_email = tk.Frame(self.khung_he_thong, bg="white")
        row_email.pack(fill="x", padx=20, pady=3)
        tk.Label(row_email, text="Email:", font=("Arial", 10), bg="white", width=16, anchor="w").pack(side="left")
        self.ent_email = tk.Entry(row_email, font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1",
                                  bd=0)
        self.ent_email.insert(0, "")
        self.ent_email.pack(side="left", fill="x", expand=True, ipady=3)

        # Ô nhập Số điện thoại
        row_sdt = tk.Frame(self.khung_he_thong, bg="white")
        row_sdt.pack(fill="x", padx=20, pady=3)
        tk.Label(row_sdt, text="Số điện thoại:", font=("Arial", 10), bg="white", width=16, anchor="w").pack(side="left")
        self.ent_sdt = tk.Entry(row_sdt, font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1", bd=0)
        self.ent_sdt.insert(0, "")
        self.ent_sdt.pack(side="left", fill="x", expand=True, ipady=3)


        self.btn_save = tk.Button(
            self.khung_he_thong, text="Lưu", font=("Arial", 11, "bold"),
            bg="#3cb3de", fg="white", bd=0,
            cursor="hand2",
            padx=15, pady=8,
        )
        self.btn_save.pack(anchor="w", padx=200, pady=15)


        # khung bao mat
        tk.Label(
            self.khung_bao_mat, text="[ BẢO MẬT ]",
            font=("Arial", 10, "bold"), fg="#3cb3de", bg="white"
        ).pack(anchor="w", padx=20, pady=(15, 5))

        tk.Frame(self.khung_bao_mat, bg="#e2e8f0", height=1).pack(fill="x", padx=20, pady=(0, 10))

        row_pass = tk.Frame(self.khung_bao_mat, bg="white")
        row_pass.pack(fill="x", padx=20, pady=3)
        tk.Label(row_pass, text="Mật khẩu:", font=("Arial", 10), bg="white", width=20, anchor="w").pack(side="left")
        self.ent_pass = tk.Entry(row_pass, show="*", font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1", bd=0)
        self.ent_pass.insert(0, "")
        self.ent_pass.pack(side="left", fill="x", expand=True, ipady=3)

        row_newpass = tk.Frame(self.khung_bao_mat, bg="white")
        row_newpass.pack(fill="x", padx=20, pady=3)
        tk.Label(row_newpass, text="Mật khẩu mới:", font=("Arial", 10), bg="white", width=20, anchor="w").pack(side="left")
        self.ent_newpass = tk.Entry(row_newpass,show="*", font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1", bd=0)
        self.ent_newpass.insert(0, "")
        self.ent_newpass.pack(side="left", fill="x", expand=True, ipady=3)

        row_renewpass = tk.Frame(self.khung_bao_mat, bg="white")
        row_renewpass.pack(fill="x", padx=20, pady=3)
        tk.Label(row_renewpass, text="Nhập lại mật khẩu mới:", font=("Arial", 10), bg="white", width=20, anchor="w").pack(side="left")
        self.ent_renewpass = tk.Entry(row_renewpass,show="*", font=("Arial", 10), highlightthickness=1, highlightbackground="#cbd5e1", bd=0)
        self.ent_renewpass.insert(0, "")
        self.ent_renewpass.pack(side="left", fill="x", expand=True, ipady=3)


        self.btn_change = tk.Button(
            self.khung_bao_mat, text="Đổi mật khẩu", font=("Arial", 11, "bold"),
            bg="#3cb3de", fg="white", bd=0,
            cursor="hand2",
            padx=15, pady=8,
        )
        self.btn_change.pack(anchor="w", padx=200, pady=15)











