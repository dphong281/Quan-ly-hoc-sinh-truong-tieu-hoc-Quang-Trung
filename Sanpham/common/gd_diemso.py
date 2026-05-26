import tkinter as tk
from tkinter import ttk


class DiemSoView:
    def __init__(self, parent, controller):
        self.master = parent
        self.controller = controller
        self.color_navy = "#1e376d"

        self.view()

    def view(self):
        self.main_frame = tk.Frame(self.master, bg="#f5f6fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            self.main_frame, text="📊 QUẢN LÝ ĐIỂM SỐ",
            font=("Arial", 16, "bold"), fg=self.color_navy, bg="#f5f6fa"
        ).pack(anchor="w", pady=(0, 15))

        toolbar = tk.Frame(self.main_frame, bg="#f5f6fa")
        toolbar.pack(fill="x", pady=(0, 15))

        left_toolbar = tk.Frame(toolbar, bg="#f5f6fa")
        left_toolbar.pack(side="left", fill="x", expand=True)

        tk.Label(left_toolbar, text=" Tìm kiếm:", font=("Arial", 10, "bold"), bg="#f5f6fa").pack(side="left")

        self.search_entry = tk.Entry(left_toolbar, font=("Arial", 10), width=30)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.insert(0, "Nhập tên, lớp hoặc mã HS...")

        self.search_entry.bind(
            "<FocusIn>",
            lambda e: self.search_entry.delete(0, "end")
            if self.search_entry.get() == "Nhập tên, lớp hoặc mã HS..."
            else None,
        )
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.tim_kiem())
        self.search_entry.bind("<Return>", lambda e: self.controller.tim_kiem())

        right_toolbar = tk.Frame(toolbar, bg="#f5f6fa")
        right_toolbar.pack(side="right")

        btn_edit = tk.Button(
            right_toolbar, text="✏️ Nhập điểm", bg="#f6c23e", fg="white",
            font=("Arial", 9, "bold"), command=self.controller.sua_diem_popup,
            padx=15, bd=0, cursor="hand2",
        )
        btn_edit.pack(side="right", padx=5)

        tree_frame = tk.Frame(self.main_frame, bg="white")
        tree_frame.pack(fill="both", expand=True)

        columns = ("STT", "ho_ten", "ma_hs", "lop", "giua_ky", "cuoi_ky", "tb_ca_nam")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)

        self.tree.heading("STT", text="STT")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("ma_hs", text="Mã HS")
        self.tree.heading("lop", text="Lớp")
        self.tree.heading("giua_ky", text="Giữa kỳ")
        self.tree.heading("cuoi_ky", text="Cuối kỳ")
        self.tree.heading("tb_ca_nam", text="TB cả năm")

        self.tree.column("STT", width=50, anchor="center")
        self.tree.column("ho_ten", width=220, anchor="w")
        self.tree.column("ma_hs", width=110, anchor="center")
        self.tree.column("lop", width=70, anchor="center")
        self.tree.column("giua_ky", width=80, anchor="center")
        self.tree.column("cuoi_ky", width=80, anchor="center")
        self.tree.column("tb_ca_nam", width=100, anchor="center")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.status_label = tk.Label(self.main_frame, text="Sẵn sàng", relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x", pady=(10, 0))