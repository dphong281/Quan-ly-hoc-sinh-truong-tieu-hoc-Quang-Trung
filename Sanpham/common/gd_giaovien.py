import customtkinter as ctk
from tkinter import ttk

class GV_View:
    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        # Màu sắc chủ đạo theo yêu cầu
        self.color_navy = "#3cb3de"

        self.view()

    def view(self):
        """Xây dựng toàn bộ giao diện bằng CustomTkinter"""
        # Frame chính
        self.main_frame = ctk.CTkFrame(self.master, fg_color="#f5f6fa", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề trang
        title_label = ctk.CTkLabel(self.main_frame, text="QUẢN LÝ GIÁO VIÊN",
                                   font=("Arial", 16, "bold"), text_color=self.color_navy)
        title_label.pack(anchor="w", pady=(0, 15))

        # Thanh công cụ
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 15))

        # --- BÊN TRÁI TOOLBAR: Tìm kiếm ---
        left_toolbar = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_toolbar.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(left_toolbar, text="Tìm kiếm:", font=("Arial", 10, "bold")).pack(side="left")

        self.search_entry = ctk.CTkEntry(left_toolbar, font=("Arial", 10), width=300, placeholder_text="Nhập tên, lớp hoặc mã gv...")
        self.search_entry.pack(side="left", padx=10)

        # Sự kiện tìm kiếm
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.tim_kiem())
        self.search_entry.bind("<Return>", lambda e: self.controller.tim_kiem())

        # --- BÊN PHẢI TOOLBAR: Các nút bấm ---
        right_toolbar = ctk.CTkFrame(toolbar, fg_color="transparent")
        right_toolbar.pack(side="right")

        # Danh sách nút bấm
        buttons = [
            ("🗑️ Xóa", "#e74a3b", self.controller.xoa),
            ("✏️ Sửa", "#f6c23e", self.controller.sua),
            ("➕ Thêm mới", "#1cc88a", self.controller.them),
            ("📂 Nhập file", "green", self.controller.import_data),
            ("📤 Xuất file", "blue", self.controller.export_data)
        ]

        for text, color, cmd in buttons:
            btn = ctk.CTkButton(right_toolbar, text=text, fg_color=color,
                                font=("Arial", 9, "bold"), width=100, command=cmd)
            btn.pack(side="right", padx=5)

        # Frame chứa bảng dữ liệu (Bọc Treeview trong CTkFrame)
        tree_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True)

        # Cấu hình Treeview
        columns = ("STT", "ho_ten", "ma_gv", "bo_mon")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        # Định nghĩa Headings
        self.tree.heading("STT", text="STT")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("ma_gv", text="Mã Giáo Viên")
        self.tree.heading("bo_mon", text="Bộ Môn")

        # Kích thước cột giữ nguyên theo yêu cầu của bạn
        self.tree.column("STT", width=60, anchor="center")
        self.tree.column("ho_ten", width=350, anchor="w")
        self.tree.column("ma_gv", width=150, anchor="center")
        self.tree.column("bo_mon", width=120, anchor="center")

        # Bind phím Delete
        self.tree.bind("<Delete>", lambda e: self.controller.xoa())

        # Thanh cuộn
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")