import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class TaiChinh(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")

        self.setup_ui()
        self.render_data()

    def setup_ui(self):
        self.configure(bg="#f0f0f0")

        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame, text="HỆ THỐNG QUẢN LÝ HỌC PHÍ",
            font=("Arial", 16, "bold"), fg="white", bg="#2c3e50"
        ).pack(pady=15)

        search_frame = tk.Frame(self, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text="Tìm kiếm học sinh:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.render_data())  # Tự lọc khi gõ chữ

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 11))
        self.search_entry.pack(side="left", padx=10, expand=True, fill="x")

        btn_reload = tk.Button(search_frame, text="🔄 Làm mới", command=self.render_data, bg="#3498db", fg="white", bd=0,
                               padx=10)
        btn_reload.pack(side="left", padx=5)

        # --- Table (Treeview) ---
        table_frame = tk.Frame(self)
        table_frame.pack(expand=True, fill="both", padx=20, pady=5)

        columns = ("id", "name", "amount", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("id", text="Mã Số")
        self.table.heading("name", text="Họ và Tên")
        self.table.heading("amount", text="Số Tiền (VNĐ)")
        self.table.heading("status", text="Trạng Thái")

        self.table.column("id", width=100, anchor="center")
        self.table.column("name", width=250)
        self.table.column("amount", width=150, anchor="e")
        self.table.column("status", width=150, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # --- Footer Actions ---
        action_frame = tk.Frame(self, bg="#f0f0f0")
        action_frame.pack(fill="x", padx=20, pady=15)

        self.btn_pay = tk.Button(
            action_frame, text="XÁC NHẬN ĐÓNG TIỀN",
            command=self.process_payment,
            bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
            padx=20, pady=10, cursor="hand2"
        )
        self.btn_pay.pack(side="right")


    def render_data(self):
        for row in self.table.get_children():
            self.table.delete(row)
        search_query = self.search_var.get().lower()

        if not os.path.exists(self.db_path):
            return  # Nếu file không tồn tại thì thoát để tránh lỗi

        try:
            with open(self.db_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Lọc dữ liệu theo tên hoặc mã
                    if search_query in row.get("ten_hs", "").lower() or search_query in row.get("ma_hs", "").lower():
                        self.table.insert("", "end", values=(
                            row.get("ma_hs"),
                            row.get("ten_hs"),
                            row.get("so_tien"),
                            row.get("trang_thai")
                        ))
        except Exception as e:
            print(f"Lỗi đọc file: {e}")


    def process_payment(self):
        """Xử lý nghiệp vụ đóng tiền"""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn học sinh cần đóng tiền!")
            return

        item = self.table.item(selected)
        ma_hs, ten_hs, _, tinh_trang = item["values"]

        if tinh_trang == "Đã đóng":
            messagebox.showinfo("Thông báo", "Học sinh {ten_hs} đã hoàn thành học phí rồi.")
            return

        if messagebox.askyesno("Xác nhận", "Xác nhận đóng tiền cho học sinh: {ten_hs}?"):
            self.update_database(ma_hs, "Đã đóng")
            self.render_data()
            messagebox.showinfo("Thành công", "Đã cập nhật trạng thái tài chính!")



    def update_database(self, ma_hs, new_status):
        data = []
        fieldnames = []
        with open(self.db_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["ma_hs"] == ma_hs:
                    row["trang_thai"] = new_status
                data.append(row)

        with open(self.db_path, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
