import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
from Sanpham.model.query import Query
from Sanpham.common.gd_diemso import DiemSoView


class DiemSoController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        # Sử dụng Model Query tập trung
        self.query = Query()
        self.hs_path = "hocsinh.csv"
        self.diem_path = "diemso.csv"

        self.view = DiemSoView(self.parent, self)
        self.tai_du_lieu()

    def tinh_tb(self, giua_ky, cuoi_ky):
        return round((giua_ky + cuoi_ky) / 2, 1)

    def kiem_tra_diem(self, text):
        try:
            diem = float(text.replace(",", "."))
            return round(diem, 1) if 0 <= diem <= 10 else None
        except ValueError:
            return None

    def tai_du_lieu(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        df_hs = self.query.read_csv(self.hs_path)
        df_diem = self.query.read_csv(self.diem_path)

        if df_hs.empty: return

        if not df_diem.empty:
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")
        else:
            df_full = df_hs
            df_full[['giua_ky', 'cuoi_ky', 'tb_ca_nam']] = ""

        for _, row in df_full.fillna("").iterrows():
            self.view.tree.insert("", "end", values=(
                row['stt'], row['ho_ten'], row['ma_hs'], row['lop'],
                row.get('giua_ky', ''), row.get('cuoi_ky', ''), row.get('tb_ca_nam', '')
            ))

    def sua_diem_popup(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn học sinh", "Vui lòng chọn một học sinh trên bảng!")
            return

        values = self.view.tree.item(selected[0])["values"]
        ho_ten, ma_hs, lop = values[1], values[2], values[3]
        giua_cu, cuoi_cu = str(values[4]), str(values[5])

        pop = tk.Toplevel(self.parent)
        pop.title("Nhập điểm học sinh")
        pop.geometry("380x320")
        pop.grab_set()

        tk.Label(pop, text=f"Học sinh: {ho_ten}", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        tk.Label(pop, text=f"Mã HS: {ma_hs}  |  Lớp: {lop}", font=("Arial", 10)).pack(pady=(0, 15))

        tk.Label(pop, text="Điểm giữa kỳ (0 - 10):").pack()
        ent_giua = tk.Entry(pop, font=("Arial", 11), width=15)
        ent_giua.pack(pady=5);
        ent_giua.insert(0, giua_cu)

        tk.Label(pop, text="Điểm cuối kỳ (0 - 10):").pack()
        ent_cuoi = tk.Entry(pop, font=("Arial", 11), width=15)
        ent_cuoi.pack(pady=5);
        ent_cuoi.insert(0, cuoi_cu)

        lbl_tb = tk.Label(pop, text="TB cả năm: --", font=("Arial", 10, "bold"), fg=self.color_navy)
        lbl_tb.pack(pady=15)

        def cap_nhat_tb(e=None):
            g, c = self.kiem_tra_diem(ent_giua.get()), self.kiem_tra_diem(ent_cuoi.get())
            if g is not None and c is not None:
                lbl_tb.config(text=f"TB cả năm: {self.tinh_tb(g, c)}")
            else:
                lbl_tb.config(text="TB cả năm: --")

        ent_giua.bind("<KeyRelease>", cap_nhat_tb)
        ent_cuoi.bind("<KeyRelease>", cap_nhat_tb)

        def luu_diem():
            g, c = self.kiem_tra_diem(ent_giua.get()), self.kiem_tra_diem(ent_cuoi.get())
            if g is None or c is None:
                messagebox.showwarning("Lỗi", "Điểm phải là số từ 0 đến 10!")
                return

            tb = self.tinh_tb(g, c)
            self.query.update_row(self.diem_path, "ma_hs", ma_hs,
                                  {"giua_ky": g, "cuoi_ky": c, "tb_ca_nam": tb})

            messagebox.showinfo("Thành công", f"Đã lưu điểm! TB: {tb}")
            pop.destroy()
            self.tai_du_lieu()

        tk.Button(pop, text="Lưu điểm", bg=self.color_navy, fg="white", command=luu_diem).pack()

    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if path:
            df_hs = self.query.read_csv(self.hs_path)
            df_diem = self.query.read_csv(self.diem_path)
            # Kết hợp dữ liệu để xuất file đầy đủ
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")
            df_full.to_excel(path, index=False)
            messagebox.showinfo("Thành công", "Đã xuất bảng điểm ra Excel!")

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            df = pd.read_excel(path)
            self.query.save_csv(df, self.diem_path)
            self.tai_du_lieu()
            messagebox.showinfo("Thành công", "Đã nhập bảng điểm từ Excel!")