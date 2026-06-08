import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class TaiChinh(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Lấy đường dẫn tuyệt đối của thư mục chứa file taichinh.py hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Đi ngược lên để tìm thư mục gốc "Sanpham", sau đó đi vào "database" và file "dongtien.csv"
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        self.db_path = os.path.join(project_root, "database", "dongtien.csv")

        self.setup_ui()
        self.render_data()

    def setup_ui(self):
        self.configure(bg="#f0f0f0")

        # --- Header ---
        header_frame = tk.Frame(self, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame, text="HỆ THỐNG QUẢN LÝ HỌC PHÍ",
            font=("Arial", 16, "bold"), fg="white", bg="#2c3e50"
        ).pack(pady=15)

        # --- Thanh tìm kiếm ---
        search_frame = tk.Frame(self, bg="#f0f0f0")
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(search_frame, text="Tìm kiếm học sinh:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")

        self.search_var = tk.StringVar()

        # Ô nhập từ khóa tìm kiếm
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 11))
        self.search_entry.pack(side="left", padx=10, expand=True, fill="x")

        # Bắt sự kiện: Khi nhấn nút Enter trên bàn phím trong ô nhập thì cũng tự tìm kiếm
        self.search_entry.bind("<Return>", lambda event: self.render_data())

        # NÚT TÌM KIẾM MỚI THÊM
        btn_search = tk.Button(search_frame, text="🔍 Tìm kiếm", command=self.render_data, bg="#2ecc71", fg="white",
                               bd=0,
                               padx=15, pady=3, font=("Arial", 10, "bold"), cursor="hand2")
        btn_search.pack(side="left", padx=5)

        # Nút làm mới danh sách
        btn_reload = tk.Button(search_frame, text="🔄 Làm mới", command=self.clear_search, bg="#3498db", fg="white",
                               bd=0,
                               padx=10, pady=3, cursor="hand2")
        btn_reload.pack(side="left", padx=5)

        # --- Bảng hiển thị dữ liệu (Treeview) ---
        table_frame = tk.Frame(self)
        table_frame.pack(expand=True, fill="both", padx=20, pady=5)

        columns = ("id", "name", "amount", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("id", text="Mã Số")
        self.table.heading("name", text="Họ và Tên")
        self.table.heading("amount", text="Số Tiền (VNĐ)")
        self.table.heading("status", text="Trạng Thái")

        # Cấu hình các cột tự động giãn khít giao diện màn hình
        self.table.column("id", width=120, anchor="center")
        self.table.column("name", width=250, stretch=True)
        self.table.column("amount", width=150, anchor="e")
        self.table.column("status", width=150, anchor="center")

        # Thanh cuộn (Scrollbar)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # --- Thanh chức năng phía dưới (Footer) ---
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
        """Đọc file CSV và hiển thị lên bảng Treeview, lọc chính xác theo từ khóa"""
        # Xóa toàn bộ dữ liệu cũ trên bảng trước khi render mới
        for row in self.table.get_children():
            self.table.delete(row)

        # Lấy từ khóa tìm kiếm (chuyển về chữ thường, xóa khoảng trắng thừa)
        search_query = self.search_var.get().lower().strip()

        if not os.path.exists(self.db_path):
            print(f"Lỗi: Không tìm thấy file dữ liệu tại đường dẫn: {self.db_path}")
            return

        try:
            with open(self.db_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                try:
                    header = next(reader)  # Bỏ qua dòng tiêu đề đầu tiên trong file CSV
                except StopIteration:
                    return  # File rỗng hoàn toàn

                for row in reader:
                    if not row or len(row) == 0:
                        continue  # Bỏ qua dòng trống nếu có

                    # Đọc chuẩn xác theo vị trí chỉ mục cột (0, 1, 2, 3)
                    ma_hs = row[0].strip() if len(row) > 0 else ""
                    ten_hs = row[1].strip() if len(row) > 1 else ""
                    so_tien = row[2].strip() if len(row) > 2 else ""
                    trang_thai = row[3].strip() if len(row) > 3 else ""

                    # Điền thông tin mặc định nếu các trường dữ liệu bị rỗng
                    if not ten_hs:
                        ten_hs = "(Chưa nhập tên)"
                    if not so_tien:
                        so_tien = "0"
                    if not trang_thai:
                        trang_thai = "Chưa đóng"

                    # BỘ LỌC TÌM KIẾM: Nếu ô tìm kiếm rỗng HOẶC từ khóa trùng với mã/tên học sinh thì mới hiển thị
                    if search_query == "" or (search_query in ten_hs.lower() or search_query in ma_hs.lower()):
                        self.table.insert("", "end", values=(ma_hs, ten_hs, so_tien, trang_thai))
        except Exception as e:
            print(f"Lỗi khi đọc file CSV: {e}")

    def clear_search(self):
        """Xóa trắng thanh tìm kiếm và tải lại toàn bộ danh sách gốc"""
        self.search_var.set("")
        self.render_data()

    def process_payment(self):
        """Xử lý chức năng cập nhật trạng thái đóng tiền khi bấm nút"""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn học sinh cần đóng tiền từ danh sách!")
            return

        item = self.table.item(selected)
        values = item.get("values", [])
        if not values:
            return

        ma_hs, ten_hs, _, tinh_trang = values

        if tinh_trang == "Đã đóng":
            messagebox.showinfo("Thông báo", f"Học sinh {ten_hs} đã hoàn thành học phí từ trước.")
            return

        if messagebox.askyesno("Xác nhận", f"Xác nhận thay đổi trạng thái đóng tiền cho học sinh: {ten_hs}?"):
            self.update_database(ma_hs, "Đã đóng")
            self.render_data()  # Cập nhật lại giao diện bảng ngay lập tức
            messagebox.showinfo("Thành công", f"Đã cập nhật trạng thái tài chính cho học sinh {ten_hs}!")

    def update_database(self, ma_hs, new_status):
        """Ghi ngược lại dữ liệu mới đã chỉnh sửa vào file CSV"""
        data = []

        if not os.path.exists(self.db_path):
            return

        try:
            # Bước 1: Đọc toàn bộ dữ liệu cũ và cập nhật dòng chỉ định
            with open(self.db_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)  # Giữ lại dòng tiêu đề ban đầu
                data.append(header)

                for row in reader:
                    if not row:
                        continue
                    # So khớp cột Mã học sinh (Cột 0) để cập nhật trạng thái mới ở Cột 3
                    if len(row) > 0 and row[0].strip() == str(ma_hs).strip():
                        while len(row) < 4:
                            row.append("")  # Đảm bảo hàng có đủ số cột để không bị lỗi IndexError
                        row[3] = new_status
                    data.append(row)

            # Bước 2: Ghi đè toàn bộ danh sách đã cập nhật vào file CSV
            with open(self.db_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
        except Exception as e:
            print(f"Lỗi khi cập nhật ghi file CSV: {e}")