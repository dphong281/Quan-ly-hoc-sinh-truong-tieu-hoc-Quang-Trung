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

        # Cấu hình stretch=True để các cột tự giãn rộng khít giao diện màn hình
        self.table.column("id", width=100, anchor="center")
        self.table.column("name", width=250, stretch=True)
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
        """Xóa bảng cũ và đọc dữ liệu dựa trên vị trí cột trong file CSV để tránh lỗi tiêu đề"""
        for row in self.table.get_children():
            self.table.delete(row)
        search_query = self.search_var.get().lower()

        if not os.path.exists(self.db_path):
            print(f"Không tìm thấy file dữ liệu tại: {self.db_path}")
            return

        try:
            with open(self.db_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)  # Bỏ qua dòng tiêu đề đầu tiên
                except StopIteration:
                    return  # File rỗng

                for row in reader:
                    if not row or len(row) == 0:
                        continue  # Bỏ qua dòng trống

                    # Đọc chuẩn xác theo số thứ tự cột trong file CSV (Cột 0, Cột 1, Cột 2, Cột 3)
                    ma_hs = row[0].strip() if len(row) > 0 else ""
                    ten_hs = row[1].strip() if len(row) > 1 else ""
                    so_tien = row[2].strip() if len(row) > 2 else ""
                    trang_thai = row[3].strip() if len(row) > 3 else ""

                    # Nếu dữ liệu các trường bị rỗng thì điền thông tin mặc định để không bị trắng bảng
                    if not ten_hs:
                        ten_hs = "(Chưa nhập tên)"
                    if not so_tien:
                        so_tien = "0"
                    if not trang_thai:
                        trang_thai = "Chưa đóng"

                    # Lọc dữ liệu theo tên hoặc mã dựa trên thanh tìm kiếm
                    if search_query in ten_hs.lower() or search_query in ma_hs.lower():
                        self.table.insert("", "end", values=(ma_hs, ten_hs, so_tien, trang_thai))
        except Exception as e:
            print(f"Lỗi đọc file: {e}")

    def process_payment(self):
        """Xử lý nghiệp vụ đóng tiền khi bấm nút"""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn học sinh cần đóng tiền!")
            return

        item = self.table.item(selected)
        values = item.get("values", [])
        if not values:
            return

        ma_hs, ten_hs, _, tinh_trang = values

        if tinh_trang == "Đã đóng":
            messagebox.showinfo("Thông báo", f"Học sinh {ten_hs} đã hoàn thành học phí rồi.")
            return

        if messagebox.askyesno("Xác nhận", f"Xác nhận đóng tiền cho học sinh: {ten_hs}?"):
            self.update_database(ma_hs, "Đã đóng")
            self.render_data()
            messagebox.showinfo("Thành công", "Đã cập nhật trạng thái tài chính!")

    def update_database(self, ma_hs, new_status):
        """Cập nhật lại trạng thái đóng tiền vào file CSV dựa trên vị trí cột"""
        data = []

        if not os.path.exists(self.db_path):
            return

        try:
            with open(self.db_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)  # Lấy dòng tiêu đề
                data.append(header)

                for row in reader:
                    if not row:
                        continue
                    # Nếu cột 0 (Mã số) trùng khớp thì cập nhật trạng thái ở cột 3
                    if len(row) > 0 and row[0].strip() == str(ma_hs).strip():
                        # Đảm bảo hàng có đủ số cột để ghi dữ liệu trạng thái
                        while len(row) < 4:
                            row.append("")
                        row[3] = new_status
                    data.append(row)

            with open(self.db_path, mode="w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
        except Exception as e:
            print(f"Lỗi ghi file: {e}")