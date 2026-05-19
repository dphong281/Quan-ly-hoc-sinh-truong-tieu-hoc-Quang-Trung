import tkinter as tk
from tkinter import ttk


class QLHSView:
    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.color_navy = "#1e376d"

        self.view()

    def view(self):
        """Xây dựng toàn bộ giao diện"""
        # Đảm bảo main_frame fill hết cấu trúc cấp trên
        self.main_frame = tk.Frame(self.master, bg="#f5f6fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề trang
        title_label = tk.Label(self.main_frame, text="📚 QUẢN LÝ HỌC SINH",
                               font=("Arial", 16, "bold"), fg=self.color_navy, bg="#f5f6fa")
        title_label.pack(anchor="w", pady=(0, 15))

        # Thanh công cụ chứa Ô tìm kiếm và TẤT CẢ các Nút bấm tập trung
        toolbar = tk.Frame(self.main_frame, bg="#f5f6fa")
        toolbar.pack(fill="x", pady=(0, 15))

        # --- BÊN TRÁI TOOLBAR: Tìm kiếm & Làm mới ---
        left_toolbar = tk.Frame(toolbar, bg="#f5f6fa")
        left_toolbar.pack(side="left", fill="x", expand=True)

        tk.Label(left_toolbar, text=" Tìm kiếm:", font=("Arial", 10, "bold"), bg="#f5f6fa").pack(side="left")

        self.search_entry = tk.Entry(left_toolbar, font=("Arial", 10), width=30)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.insert(0, "Nhập tên, lớp hoặc mã HS...")

        # Sự kiện tìm kiếm gọi sang controller
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0, 'end') if self.search_entry.get() == "Nhập tên, lớp hoặc mã HS..." else None)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.search_data())
        self.search_entry.bind("<Return>", lambda e: self.controller.search_data())

        # --- BÊN PHẢI TOOLBAR: Đẩy toàn bộ nút sửa xóa lên đây ---
        right_toolbar = tk.Frame(toolbar, bg="#f5f6fa")
        right_toolbar.pack(side="right")

        # Nút Xóa (Màu đỏ)
        btn_delete = tk.Button(right_toolbar, text="🗑️ Xóa", bg="#e74a3b", fg="white",
                               font=("Arial", 9, "bold"), command=self.controller.delete_student, padx=15, bd=0, cursor="hand2")
        btn_delete.pack(side="right", padx=5)

        # Nút Sửa (Màu cam/vàng)
        btn_edit = tk.Button(right_toolbar, text="✏️ Sửa", bg="#f6c23e", fg="white",
                             font=("Arial", 9, "bold"), command=self.controller.edit_student_popup, padx=15, bd=0, cursor="hand2")
        btn_edit.pack(side="right", padx=5)

        # Nút Thêm mới (Màu xanh lá)
        btn_add = tk.Button(right_toolbar, text="➕ Thêm mới", bg="#1cc88a", fg="white",
                            font=("Arial", 9, "bold"), command=self.controller.add_student_popup, padx=15, bd=0, cursor="hand2")
        btn_add.pack(side="right", padx=5)

        # Frame chứa bảng dữ liệu Treeview
        tree_frame = tk.Frame(self.main_frame, bg="white")
        # QUAN TRỌNG: Cần expand=True để chiếm trọn không gian trống giữa toolbar và status_label
        tree_frame.pack(fill="both", expand=True)

        columns = ("STT", "ho_ten", "ma_hs", "lop")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        # Định nghĩa Headings
        self.tree.heading("STT", text="STT")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("ma_hs", text="Mã Học Sinh")
        self.tree.heading("lop", text="Lớp")

        # Định nghĩa kích thước các Column
        self.tree.column("STT", width=60, anchor="center")
        self.tree.column("ho_ten", width=350, anchor="w")
        self.tree.column("ma_hs", width=150, anchor="center")
        self.tree.column("lop", width=120, anchor="center")

        # Bind phím Delete nhanh trên bàn phím
        self.tree.bind("<Delete>", lambda e: self.controller.delete_student())

        # Thanh cuộn dọc
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Thanh trạng thái Status bar dưới cùng
        self.status_label = tk.Label(self.main_frame, text="Sẵn sàng", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x", pady=(10, 0))