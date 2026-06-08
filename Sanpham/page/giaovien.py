import tkinter as tk
import threading
from tkinter import messagebox, filedialog
import pandas as pd
from Sanpham.model.query import Query
from Sanpham.common.gd_giaovien import GV_View
from Sanpham.assets.loading import LoadingScreen  # Import LoadingScreen


class GV_Controller:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        # Kết nối với Model Query dùng chung
        self.query = Query()
        self.csv_file = "giaovien.csv"

        self.view = GV_View(self.parent, self)

        # Khởi tạo LoadingScreen
        self.loading_screen = LoadingScreen(self.parent)

        # Gọi tải dữ liệu bất đồng bộ
        self.load_data_async()
        self.load_data()

    def load_data_async(self):
        """Hàm khởi tạo việc tải dữ liệu (Chạy ở Main Thread)"""
        self.loading_screen.show()  # 1. Hiện loading
        threading.Thread(target=self._xu_ly_load_data, daemon=True).start()  # 2. Chạy Thread

    def _xu_ly_load_data(self):
        """Hàm xử lý dữ liệu nặng (Chạy ở Worker Thread)"""
        data = self.query.get_all(self.csv_file)
        # 3. Gửi dữ liệu về Main Thread để vẽ giao diện
        self.parent.after(0, lambda: self._hoan_thanh_load_data(data))

    def _hoan_thanh_load_data(self, data):
        """Hàm cập nhật giao diện (Chạy ở Main Thread)"""
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in data:
            self.view.tree.insert("", "end", values=(
                row.get('stt'), row.get('ho_ten'),
                row.get('ma_gv'), row.get('bo_mon')
            ))
        self.loading_screen.hide()  # 4. Tắt loading

    def xoa(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn giáo viên cần xóa!")
            return

        ma_gv = self.view.tree.item(selected[0])['values'][2]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa giáo viên này?"):
            self.query.delete_row(self.csv_file, "ma_gv", ma_gv)
            self.load_data_async()  # Dùng hàm async
            messagebox.showinfo("Thành công", "Đã xóa giáo viên!")


    def them(self):
        self.teacher_form_popup(None)

    def sua(self):
        selected = self.view.tree.selection()
        if selected:
            v = self.view.tree.item(selected[0])['values']
            self.teacher_form_popup({"ho_ten": v[1], "ma_gv": v[2], "bo_mon": v[3]})

    def tim_kiem(self):
        query = self.view.search_entry.get().lower()
        self.load_data()
        if query and query != "nhập tên, lớp hoặc mã gv...":
            for item in self.view.tree.get_children():
                v = self.view.tree.item(item)['values']
                if query not in str(v[1]).lower() and query not in str(v[2]).lower() and query not in str(v[3]).lower():
                    self.view.tree.delete(item)

    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if not path: return
        self.loading_screen.show()

        def _task_export():
            self.query.read_csv(self.csv_file).to_excel(path, index=False)
            self.parent.after(0, self.loading_screen.hide)

        threading.Thread(target=_task_export, daemon=True).start()

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return

        self.loading_screen.show()

        def _task_import():
            try:
                # 1. Đọc file (Công việc nặng - chạy ở luồng phụ)
                df = pd.read_excel(path)
                self.query.save_csv(df, self.csv_file)

                # 2. Quay về luồng chính để cập nhật GUI
                self.parent.after(0, lambda: self.loading_screen.hide())
                self.parent.after(0, self.load_data)  # Load lại dữ liệu lên Treeview
                self.parent.after(0, lambda: messagebox.showinfo("Thành công", "Đã nhập bảng excel!"))

            except Exception as e:
                # Nếu có lỗi, cũng phải đưa thông báo về luồng chính
                self.parent.after(0, lambda: self.loading_screen.hide())
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể nhập file: {e}"))

        # Khởi chạy luồng
        threading.Thread(target=_task_import, daemon=True).start()

    def load_data(self):
        """Xóa bảng cũ và nạp lại dữ liệu từ file CSV"""
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        data = self.query.get_all(self.csv_file)

        for row in data:
            self.view.tree.insert("", "end", values=(
                row.get('stt'), row.get('ho_ten'),
                row.get('ma_gv'), row.get('bo_mon')
            ))

    def teacher_form_popup(self, teacher_data=None):
        pop = tk.Toplevel(self.parent)
        pop.title("Thêm/Sửa giáo viên")
        pop.geometry("300x300")

        entries = {"name": tk.Entry(pop), "id": tk.Entry(pop), "subject": tk.Entry(pop)}
        tk.Label(pop, text="Họ tên:").pack();
        entries["name"].pack()
        tk.Label(pop, text="Mã GV:").pack();
        entries["id"].pack()
        tk.Label(pop, text="Bộ môn:").pack();
        entries["subject"].pack()

        if teacher_data:
            entries["name"].insert(0, teacher_data["ho_ten"])
            entries["id"].insert(0, teacher_data["ma_gv"])
            entries["id"].config(state="disabled")  # Không cho sửa Mã GV
            entries["subject"].insert(0, teacher_data["bo_mon"])

        # Hàm kiểm tra tên không chứa số/ký tự đặc biệt (Không dùng Regex)
        def kiem_tra_ten(chuoi):
            for char in chuoi:
                if not char.isalpha() and not char.isspace():
                    return False
            return True

        def luu():
            ho_ten = entries["name"].get().strip()
            ma_gv = entries["id"].get().strip()
            bo_mon = entries["subject"].get().strip()

            # 1. Kiểm tra trống
            if not ho_ten or not ma_gv or not bo_mon:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return

            # 3. Kiểm tra tên không chứa số/ký tự đặc biệt
            if not kiem_tra_ten(ho_ten):
                messagebox.showerror("Lỗi", "Tên giáo viên không được chứa số hoặc ký tự đặc biệt!")
                return

            df = self.query.read_csv(self.csv_file)

            # 4. Kiểm tra trùng Mã GV (chỉ check khi thêm mới)
            if not teacher_data:
                if ma_gv in df["ma_gv"].astype(str).values:
                    messagebox.showerror("Lỗi", "Mã giáo viên này đã tồn tại!")
                    return

            # Thực hiện lưu
            if teacher_data:  # Chế độ Sửa
                self.query.update_row(self.csv_file, "ma_gv", ma_gv,
                                      {"ho_ten": ho_ten, "bo_mon": bo_mon})
            else:  # Chế độ Thêm mới
                new_row = pd.DataFrame([{"stt": len(df) + 1, "ho_ten": ho_ten,
                                         "ma_gv": ma_gv, "bo_mon": bo_mon}])
                df = pd.concat([df, new_row], ignore_index=True)
                self.query.save_csv(df, self.csv_file)

            pop.destroy()
            self.load_data_async()
            messagebox.showinfo("Thành công", "Đã lưu thông tin giáo viên!")

        tk.Button(pop, text="Lưu", command=luu).pack(pady=15)
