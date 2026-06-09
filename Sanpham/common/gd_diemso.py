import customtkinter as ctk
from tkinter import ttk

class DiemSoView:
    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.color_navy = "#1e376d"
        self.view()

    def view(self):
        # Sử dụng CTkFrame làm nền chính
        self.main_frame = ctk.CTkFrame(self.master, fg_color="#f5f6fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        ctk.CTkLabel(
            self.main_frame, text=" QUẢN LÝ ĐIỂM SỐ",
            font=("Arial", 20, "bold"), text_color=self.color_navy
        ).pack(anchor="w", pady=(0, 15))

        # Toolbar
        toolbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 15))

        # Tìm kiếm
        ctk.CTkLabel(toolbar, text="Tìm kiếm:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(toolbar, placeholder_text="Nhập tên, lớp hoặc mã HS...", width=300)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.tim_kiem())

        # Button nhóm phải
        btn_export = ctk.CTkButton(toolbar, text=" Xuất Excel", fg_color="#007bff", width=120, command=self.controller.export_data)
        btn_export.pack(side="right", padx=5)

        btn_import = ctk.CTkButton(toolbar, text=" Nhập Excel", fg_color="#28a745", width=120, command=self.controller.import_data)
        btn_import.pack(side="right", padx=5)

        btn_edit = ctk.CTkButton(toolbar, text="✏ Nhập điểm", fg_color="#f6c23e", text_color="white", width=120, command=self.controller.sua_diem_popup)
        btn_edit.pack(side="right", padx=5)

        # Bảng dữ liệu
        tree_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        tree_frame.pack(fill="both", expand=True)

        columns = ("STT", "ho_ten", "ma_hs", "lop", "giua_ky", "cuoi_ky", "tb_ca_nam")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        # Cấu hình tiêu đề cột
        headers = ["STT", "Họ và Tên", "Mã HS", "Lớp", "Giữa kỳ", "Cuối kỳ", "TB cả năm"]
        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=100 if col != "ho_ten" else 220, anchor="center")
        self.tree.column("ho_ten", anchor="w")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        sb.pack(side="right", fill="y")