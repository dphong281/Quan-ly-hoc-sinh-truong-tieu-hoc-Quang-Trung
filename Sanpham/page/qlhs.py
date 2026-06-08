import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from Sanpham.model.query import Query
from Sanpham.common.gd_qlhs import QLHSView


class QLHSController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        # Kết nối với Model Query dùng chung
        self.query = Query()
        self.csv_file = "hocsinh.csv"

        self.view = QLHSView(self.parent, self)
        self.load_data()

    def load_data(self):
        """Xóa bảng cũ và nạp lại dữ liệu từ file CSV"""
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
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa học sinh!")

    def student_form_popup(self, student_data=None):
        pop = tk.Toplevel(self.parent)
        pop.title("Thêm/Sửa học sinh")
        pop.geometry("300x250")

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
            df = self.query.read_csv(self.csv_file)

            if student_data:  # Chế độ Sửa
                self.query.update_row(self.csv_file, "ma_hs", entries["id"].get(),
                                      {"ho_ten": entries["name"].get(), "lop": entries["class"].get()})
            else:  # Chế độ Thêm mới
                new_row = pd.DataFrame([{"stt": len(df) + 1, "ho_ten": entries["name"].get(),
                                         "ma_hs": entries["id"].get(), "lop": entries["class"].get()}])
                df = pd.concat([df, new_row], ignore_index=True)
                self.query.save_csv(df, self.csv_file)

            pop.destroy()
            self.load_data()

        tk.Button(pop, text="Lưu", command=luu).pack(pady=15)

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
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if path:
            df = pd.read_excel(path)
            self.query.save_csv(df, self.csv_file)
            self.load_data()
            messagebox.showinfo("Thành công", "Đã nhập Excel!")