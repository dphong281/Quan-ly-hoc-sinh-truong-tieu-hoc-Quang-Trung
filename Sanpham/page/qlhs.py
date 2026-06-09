import tkinter as tk
import threading
from tkinter import messagebox, filedialog
import pandas as pd
from Sanpham.model.query import Query
from Sanpham.common.gd_qlhs import QLHSView
from Sanpham.assets.loading import LoadingScreen
import re


class QLHSController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        self.query = Query()
        self.csv_file = "hocsinh.csv"

        self.view = QLHSView(self.parent, self)
        self.load_data()

        self.loading_screen = LoadingScreen(parent)

        self.load_data_async()

    def load_data_async(self):
        self.loading_screen.show()
        threading.Thread(target=self._xu_ly_load_data, daemon=True).start()  # 2. Chạy Thread

    def _xu_ly_load_data(self):
        data = self.query.get_all(self.csv_file)

        self.parent.after(0, lambda: self._hoan_thanh_load_data(data))

    def _hoan_thanh_load_data(self, data):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in data:
            self.view.tree.insert("", "end", values=(
                row.get('stt'), row.get('ho_ten'),
                row.get('ma_hs'), row.get('lop')
            ))

        self.loading_screen.hide()


    def load_data(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        data = self.query.get_all(self.csv_file)

        for row in data:
            self.view.tree.insert("", "end", values=(
                row.get('stt'), row.get('ho_ten'),
                row.get('ma_hs'), row.get('lop')
            ))

    def xoa(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn học sinh cần xóa!")
            return

        ma_hs = self.view.tree.item(selected[0])['values'][2]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa học sinh này?"):
            self.query.delete_row(self.csv_file, "ma_hs", ma_hs)
            self.load_data_async()
            messagebox.showinfo("Thành công", "Đã xóa học sinh!")

    def them(self):
        self.student_form_popup(None)

    def sua(self):
        selected = self.view.tree.selection()
        if selected:
            v = self.view.tree.item(selected[0])['values']
            self.student_form_popup({"ho_ten": v[1], "ma_hs": v[2], "lop": v[3]})

    def tim_kiem(self):
        query = self.view.search_entry.get().lower()
        self.load_data()
        if query and query != "nhập tên, lớp hoặc mã hs...":
            for item in self.view.tree.get_children():
                v = self.view.tree.item(item)['values']
                if query not in str(v[1]).lower() and query not in str(v[2]).lower() and query not in str(v[3]).lower():
                    self.view.tree.delete(item)

    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if path:
            self.query.read_csv(self.csv_file).to_excel(path, index=False)
            messagebox.showinfo("Thành công", "Đã xuất Excel!")

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return

        self.loading_screen.show()

        def _task_import():
            try:
                df = pd.read_excel(path)
                self.query.save_csv(df, self.csv_file)

                self.parent.after(0, self.loading_screen.hide)
                self.parent.after(0, self.load_data_async)
                self.parent.after(0, lambda: messagebox.showinfo("Thành công", "Đã nhập dữ liệu từ Excel!"))

            except Exception as e:
                self.parent.after(0, self.loading_screen.hide)
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể nhập file: {e}"))

        threading.Thread(target=_task_import, daemon=True).start()

    def student_form_popup(self, student_data=None):
        pop = tk.Toplevel(self.parent)
        pop.title("Thêm/Sửa học sinh")
        pop.geometry("300x300")

        entries = {"name": tk.Entry(pop), "id": tk.Entry(pop), "class": tk.Entry(pop)}
        tk.Label(pop, text="Họ tên:").pack();
        entries["name"].pack()
        tk.Label(pop, text="Mã HS:").pack();
        entries["id"].pack()
        tk.Label(pop, text="Lớp:").pack();
        entries["class"].pack()

        if student_data:
            entries["name"].insert(0, student_data["ho_ten"])
            entries["id"].insert(0, student_data["ma_hs"])
            entries["id"].config(state="disabled")
            entries["class"].insert(0, student_data["lop"])

        def luu():
            ho_ten = entries["name"].get().strip()
            ma_hs = entries["id"].get().strip()
            lop = entries["class"].get().strip()

            # Không để trống
            if not ho_ten or not ma_hs or not lop:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return

            if not re.match(r'^[a-zA-ZÀ-Ỹà-ỹ\s]+$', ho_ten):
                messagebox.showerror("Lỗi", "Tên học sinh không được chứa ký tự đặc biệt hoặc số!")
                return

            # Kiểm tra trùng Mã HS (Chỉ check khi thêm mới)
            if not student_data:
                df_check = self.query.read_csv(self.csv_file)
                if ma_hs in df_check["ma_hs"].astype(str).values:
                    messagebox.showerror("Lỗi", "Mã học sinh này đã tồn tại!")
                    return

            # LƯU
            df = self.query.read_csv(self.csv_file)
            if student_data:
                self.query.update_row(self.csv_file, "ma_hs", ma_hs,
                                      {"ho_ten": ho_ten, "lop": lop})
            else:
                new_row = pd.DataFrame([{"stt": len(df) + 1, "ho_ten": ho_ten,
                                         "ma_hs": ma_hs, "lop": lop}])
                df = pd.concat([df, new_row], ignore_index=True)
                self.query.save_csv(df, self.csv_file)

            pop.destroy()
            self.load_data_async()
            messagebox.showinfo("Thành công", "Đã lưu thông tin!")

        tk.Button(pop, text="Lưu", command=luu).pack(pady=15)