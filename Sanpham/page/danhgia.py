import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
import os


class DanhGiaView:
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance

        # Khởi tạo đường dẫn chính xác tới các file database csv của bạn
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.hocsinh_file = os.path.normpath(os.path.join(self.dir_path, "..", "database", "hocsinh.csv"))
        self.diemso_file = os.path.normpath(os.path.join(self.dir_path, "..", "database", "diemso.csv"))

        # --- TIÊU ĐỀ TRANG ---
        title_label = ctk.CTkLabel(
            self.master,
            text="📑 ĐÁNH GIÁ VÀ XẾP LOẠI HỌC SINH",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="#1A365D"
        )
        title_label.pack(anchor="w", padx=25, pady=(20, 10))

        # --- THANH TÌM KIẾM ---
        search_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        search_frame.pack(fill="x", padx=25, pady=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nhập mã học sinh để lọc...",
            width=280
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.load_data())

        btn_search = ctk.CTkButton(search_frame, text="Tìm kiếm", command=self.load_data, width=100)
        btn_search.pack(side="left", padx=5)

        btn_refresh = ctk.CTkButton(search_frame, text="Làm mới", fg_color="gray", command=self.refresh_search,
                                    width=100)
        btn_refresh.pack(side="left", padx=5)

        # --- BẢNG HIỂN THỊ DỮ LIỆU (TREEVIEW) ---
        table_frame = ctk.CTkFrame(self.master, fg_color="white", corner_radius=8)
        table_frame.pack(fill="both", expand=True, padx=25, pady=(10, 25))

        columns = ("stt", "ma_hs", "ho_ten", "lop", "tb_ca_nam", "xep_loai")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("stt", text="STT")
        self.tree.heading("ma_hs", text="Mã Học Sinh")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("lop", text="Lớp")
        self.tree.heading("tb_ca_nam", text="ĐTB Cả Năm")
        self.tree.heading("xep_loai", text="Xếp Loại")

        self.tree.column("stt", width=60, anchor="center")
        self.tree.column("ma_hs", width=120, anchor="center")
        self.tree.column("ho_ten", width=220, anchor="w")
        self.tree.column("lop", width=100, anchor="center")
        self.tree.column("tb_ca_nam", width=120, anchor="center")
        self.tree.column("xep_loai", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")

        # Nạp dữ liệu tự động lên bảng ngay khi mở trang
        self.load_data()

    def doc_file_csv(self, file_path):
        data = []
        if not os.path.exists(file_path):
            return data
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({k.strip(): v.strip() for k, v in row.items() if k})
        return data

    def tinh_xep_loai(self, diem_str):
        try:
            diem = float(diem_str)
            if diem >= 8.0:
                return "Giỏi"
            elif diem >= 6.5:
                return "Khá"
            elif diem >= 5.0:
                return "Trung bình"
            else:
                return "Yếu"
        except:
            return "Chưa có điểm"

    def refresh_search(self):
        self.search_entry.delete(0, 'end')
        self.load_data()

    def load_data(self):
        # Xóa dữ liệu cũ trên bảng trước khi nạp dữ liệu mới
        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = self.search_entry.get().strip().lower()
        list_hocsinh = self.doc_file_csv(self.hocsinh_file)
        list_diemso = self.doc_file_csv(self.diemso_file)

        # Tạo từ điển điểm để map nhanh theo mã học sinh
        dict_diem = {d.get("ma_hs"): d.get("tb_ca_nam", "0") for d in list_diemso if d.get("ma_hs")}

        stt = 1
        for hs in list_hocsinh:
            ma_hs = hs.get("ma_hs", "")
            ho_ten = hs.get("ho_ten", "")
            lop = hs.get("lop", "")

            # Nếu có nhập từ khóa tìm kiếm thì lọc theo Mã học sinh
            if keyword and (keyword not in ma_hs.lower()):
                continue

            tb_ca_nam = dict_diem.get(ma_hs, "N/A")
            xep_loai = self.tinh_xep_loai(tb_ca_nam) if tb_ca_nam != "N/A" else "Chưa có điểm"

            self.tree.insert("", "end", values=(stt, ma_hs, ho_ten, lop, tb_ca_nam, xep_loai))
            stt += 1