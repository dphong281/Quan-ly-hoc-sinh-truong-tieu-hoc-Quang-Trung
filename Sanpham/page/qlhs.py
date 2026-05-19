import tkinter as tk
from tkinter import messagebox
import os

from Sanpham.model.hocsinh import HocSinhModel
from Sanpham.common.gd_qlhs import QLHSView  # Nhập giao diện từ file gd_qlhs.py vào


class QLHSController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        # Thiết lập đường dẫn database CSV gốc của bạn
        current_dir = os.path.dirname(__file__)
        self.csv_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")

        # Khởi tạo Model dữ liệu
        self.hs = HocSinhModel(self.csv_path, ["stt", "ho_ten", "ma_hs", "lop"])

        # KHẮC PHỤC LỖI: Truyền cả parent và chính controller này (self) vào giao diện
        self.view = QLHSView(self.parent, self)

        # Tải dữ liệu lên bảng ngay khi chạy
        self.load_data()

    def load_data(self):
        """Tải dữ liệu từ Model học sinh và nạp thẳng vào Treeview của Giao diện"""
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        result = self.hs.list()
        data = result["data"]

        for row in data:
            stt_raw = str(row.get('stt', ''))
            stt_final = stt_raw.split('.')[0] if '.' in stt_raw else stt_raw

            self.view.tree.insert("", "end", values=(
                stt_final,
                row.get('ho_ten', ''),
                row.get('ma_hs', ''),
                row.get('lop', '')
            ))

    def delete_student(self):
        """Xử lý xóa dòng đang được chọn từ bảng"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn học sinh", "Vui lòng chọn một học sinh trên bảng để xóa!")
            return

        values = self.view.tree.item(selected[0])['values']
        student_name = values[1]
        ma_hs = values[2]

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa học sinh '{student_name}'?"):
            self.hs.delete("ma_hs", ma_hs)
            self.view.tree.delete(selected[0])
            self.view.status_label.config(text=f"Đã xóa học sinh: {student_name}")
            self.load_data()  # Đồng bộ lại STT chuẩn sau khi xóa

    def student_form_popup(self, student_data=None):
        """Form Popup dùng chung cho cả Thêm mới và Chỉnh sửa thông tin"""
        is_edit = student_data is not None

        pop = tk.Toplevel(self.parent)
        pop.title("Sửa thông tin học sinh" if is_edit else "Thêm học sinh mới")
        pop.geometry("350x300")
        pop.grab_set()

        fields = [("Họ và Tên:", "name"), ("Mã Học Sinh:", "id"), ("Lớp:", "class")]
        entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(pop, text=label, font=("Arial", 10)).pack(pady=(10, 0))
            entries[key] = tk.Entry(pop, font=("Arial", 10), width=30)
            entries[key].pack(pady=5)

        # Nếu là chế độ SỬA: Đổ dữ liệu cũ vào các ô và khóa ô Mã HS lại
        if is_edit:
            entries["name"].insert(0, student_data["ho_ten"])
            entries["id"].insert(0, student_data["ma_hs"])
            entries["class"].insert(0, student_data["lop"])
            entries["id"].config(state="disabled")
            entries["name"].focus_set()
        else:
            entries["name"].focus_set()

        def save_action():
            name = entries["name"].get().strip()
            mshs = entries["id"].get().strip()
            lop = entries["class"].get().strip()

            if not name or not mshs or not lop:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các thông tin!")
                return

            if is_edit:
                # Logic Sửa: Xóa cái cũ đi, ghi đè cái mới vào
                self.hs.delete("ma_hs", student_data["ma_hs"])
                updated_student = {"stt": student_data["stt"], "ho_ten": name, "ma_hs": student_data["ma_hs"],
                                   "lop": lop}
                self.hs.insert(updated_student)
                self.view.status_label.config(text=f"Đã cập nhật thông tin học sinh: {name}")
                messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
            else:
                # Logic Thêm mới
                current_count = len(self.view.tree.get_children(""))
                new_student = {"stt": str(current_count + 1), "ho_ten": name, "ma_hs": mshs, "lop": lop}
                self.hs.insert(new_student)
                self.view.status_label.config(text=f"Đã thêm học sinh mới: {name}")
                messagebox.showinfo("Thành công", f"Đã thêm học sinh {name}")

            pop.destroy()
            self.load_data()

        pop.bind("<Return>", lambda e: save_action())
        btn_text = "Cập nhật thông tin" if is_edit else "Lưu thông tin"
        tk.Button(pop, text=btn_text, bg=self.color_navy, fg="white",
                  font=("Arial", 10, "bold"), command=save_action, pady=8, padx=20).pack(pady=20)

    def add_student_popup(self):
        """Nút 'Thêm' từ giao diện gọi hàm này"""
        self.student_form_popup(student_data=None)

    def edit_student_popup(self):
        """Nút 'Sửa' từ giao diện gọi hàm này"""
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn học sinh", "Vui lòng chọn một học sinh trên bảng để sửa!")
            return

        values = self.view.tree.item(selected[0])['values']
        # Đóng gói dữ liệu dòng được chọn thành một Dictonary để truyền đi
        selected_student = {
            "stt": values[0],
            "ho_ten": values[1],
            "ma_hs": values[2],
            "lop": values[3]
        }
        self.student_form_popup(student_data=selected_student)

    # =========================================================================

    def search_data(self):
        """Logic tìm kiếm dữ liệu"""
        query = self.view.search_entry.get().lower()
        if query == "nhập tên, lớp hoặc mã hs...":
            return

        self.load_data()
        if query:
            for item in self.view.tree.get_children():
                v = self.view.tree.item(item)['values']
                if query not in str(v[1]).lower() and query not in str(v[2]).lower() and query not in str(v[3]).lower():
                    self.view.tree.delete(item)