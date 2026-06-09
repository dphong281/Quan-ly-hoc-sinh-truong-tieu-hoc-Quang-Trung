import customtkinter as ctk
from tkinter import ttk


class QLHSView:
    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.color_navy = "#3cb3de"

        self.view()

    def view(self):

        self.main_frame = ctk.CTkFrame(self.master, fg_color="#f5f6fa", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        title_label = ctk.CTkLabel(self.main_frame, text="QUẢN LÝ HỌC SINH", font=("Arial", 16, "bold"), text_color=self.color_navy)
        title_label.pack(anchor="w", pady=(0, 15))

        # Toolbar
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 15))

        # LEFT TOOLBAR: Tìm kiếm
        left_toolbar = ctk.CTkFrame(toolbar, fg_color="transparent")
        left_toolbar.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(left_toolbar, text="Tìm kiếm:").pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(left_toolbar, placeholder_text="Nhập tên, lớp hoặc mã HS...", width=300)
        self.search_entry.pack(side="left", padx=10)

        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.tim_kiem())

        #  RIGHT TOOLBAR: Nút bấm
        right_toolbar = ctk.CTkFrame(toolbar, fg_color="transparent")
        right_toolbar.pack(side="right")

        # Nút bấm
        ctk.CTkButton(right_toolbar, text=" Xóa", fg_color="#e74a3b", width=80, command=self.controller.xoa).pack(
            side="right", padx=5)
        ctk.CTkButton(right_toolbar, text=" Sửa", fg_color="#f6c23e", width=80, command=self.controller.sua).pack(
            side="right", padx=5)
        ctk.CTkButton(right_toolbar, text=" Thêm mới", fg_color="#1cc88a", width=100,
                      command=self.controller.them).pack(side="right", padx=5)
        ctk.CTkButton(right_toolbar, text="Nhập file", fg_color="green", width=90,
                      command=self.controller.import_data).pack(side="right", padx=5)
        ctk.CTkButton(right_toolbar, text="Xuất file", fg_color="blue", width=90,
                      command=self.controller.export_data).pack(side="right", padx=5)

        # Frame chứa bảng dữ liệu
        tree_frame = ctk.CTkFrame(self.main_frame, fg_color="white", border_width=1, border_color="#e2e8f0")
        tree_frame.pack(fill="both", expand=True)

        columns = ("STT", "ho_ten", "ma_hs", "lop")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        self.tree.heading("STT", text="STT")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("ma_hs", text="Mã Học Sinh")
        self.tree.heading("lop", text="Lớp")

        self.tree.column("STT", width=60, anchor="center")
        self.tree.column("ho_ten", width=350, anchor="w")
        self.tree.column("ma_hs", width=150, anchor="center")
        self.tree.column("lop", width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)