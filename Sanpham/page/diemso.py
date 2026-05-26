import csv
import os
import tkinter as tk
from tkinter import messagebox

from Sanpham.common.gd_diemso import DiemSoView


class DiemSoController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        current_dir = os.path.dirname(__file__)
        db_dir = os.path.join(os.path.dirname(current_dir), "database")

        self.hs_path = os.path.join(db_dir, "hocsinh.csv")
        self.diem_path = os.path.join(db_dir, "diemso.csv")

        self.view = DiemSoView(self.parent, self)
        self.tai_du_lieu()

    def tinh_tb(self, giua_ky, cuoi_ky):
        return round((giua_ky + cuoi_ky) / 2, 1)

    def doc_diem(self):
        diem_dict = {}
        if not os.path.exists(self.diem_path):
            return diem_dict

        with open(self.diem_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ma = (row.get("ma_hs") or "").strip()
                if not ma: continue
                diem_dict[ma] = {
                    "giua_ky": (row.get("giua_ky") or "").strip(),
                    "cuoi_ky": (row.get("cuoi_ky") or "").strip(),
                    "tb_ca_nam": (row.get("tb_ca_nam") or "").strip(),
                }
        return diem_dict

    def ghi_diem_file(self, diem_dict):
        with open(self.diem_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["ma_hs", "giua_ky", "cuoi_ky", "tb_ca_nam"])
            writer.writeheader()
            for ma_hs in sorted(diem_dict.keys()):
                row = diem_dict[ma_hs]
                writer.writerow({
                    "ma_hs": ma_hs,
                    "giua_ky": row["giua_ky"],
                    "cuoi_ky": row["cuoi_ky"],
                    "tb_ca_nam": row["tb_ca_nam"],
                })

    def doc_hocsinh(self):
        ds = []
        if not os.path.exists(self.hs_path):
            return ds

        with open(self.hs_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                ma_hs = clean.get("ma_hs", "")
                ho_ten = clean.get("ho_ten", "")
                if not ma_hs or not ho_ten: continue
                stt_raw = str(clean.get("stt", ""))
                stt = stt_raw.split(".")[0] if "." in stt_raw else stt_raw
                ds.append({
                    "stt": stt,
                    "ho_ten": ho_ten,
                    "ma_hs": ma_hs,
                    "lop": clean.get("lop", ""),
                })
        return ds

    def tai_du_lieu(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        diem_dict = self.doc_diem()
        for hs in self.doc_hocsinh():
            ma = hs["ma_hs"]
            diem = diem_dict.get(ma, {})
            self.view.tree.insert("", "end", values=(
                hs["stt"], hs["ho_ten"], ma, hs["lop"],
                diem.get("giua_ky", ""), diem.get("cuoi_ky", ""), diem.get("tb_ca_nam", ""),
            ))

    def tim_kiem(self):
        query = self.view.search_entry.get().lower()
        if query == "nhập tên, lớp hoặc mã hs...": return

        self.tai_du_lieu()
        if query:
            for item in self.view.tree.get_children():
                v = self.view.tree.item(item)["values"]
                if (query not in str(v[1]).lower() and query not in str(v[2]).lower() and query not in str(
                        v[3]).lower()):
                    self.view.tree.delete(item)

    def kiem_tra_diem(self, text):
        try:
            diem = float(text.replace(",", "."))
        except ValueError:
            return None
        if diem < 0 or diem > 10: return None
        return round(diem, 1)

    def sua_diem_popup(self):
        selected = self.view.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn học sinh", "Vui lòng chọn một học sinh trên bảng!")
            return

        values = self.view.tree.item(selected[0])["values"]
        ho_ten, ma_hs, lop = values[1], values[2], values[3]
        giua_cu, cuoi_cu = str(values[4]) if len(values) > 4 else "", str(values[5]) if len(values) > 5 else ""

        pop = tk.Toplevel(self.parent)
        pop.title("Nhập điểm học sinh")
        pop.geometry("380x320")
        pop.grab_set()

        tk.Label(pop, text=f"Học sinh: {ho_ten}", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        tk.Label(pop, text=f"Mã HS: {ma_hs}  |  Lớp: {lop}", font=("Arial", 10)).pack(
            pady=(0, 15))

        tk.Label(pop, text="Điểm giữa kỳ (0 - 10):", font=("Arial", 10)).pack()
        ent_giua = tk.Entry(pop, font=("Arial", 11), width=15)
        ent_giua.pack(pady=5)
        ent_giua.insert(0, giua_cu)

        tk.Label(pop, text="Điểm cuối kỳ (0 - 10):", font=("Arial", 10)).pack(pady=(10, 0))
        ent_cuoi = tk.Entry(pop, font=("Arial", 11), width=15)
        ent_cuoi.pack(pady=5)
        ent_cuoi.insert(0, cuoi_cu)

        lbl_tb = tk.Label(pop, text="TB cả năm: --", font=("Arial", 10, "bold"), fg=self.color_navy)
        lbl_tb.pack(pady=15)

        def cap_nhat_tb_label():
            g = self.kiem_tra_diem(ent_giua.get().strip())
            c = self.kiem_tra_diem(ent_cuoi.get().strip())
            if g is not None and c is not None:
                lbl_tb.config(text=f"TB cả năm: {self.tinh_tb(g, c)}")
            else:
                lbl_tb.config(text="TB cả năm: --")

        ent_giua.bind("<KeyRelease>", lambda e: cap_nhat_tb_label())
        ent_cuoi.bind("<KeyRelease>", lambda e: cap_nhat_tb_label())
        cap_nhat_tb_label()

        def luu_diem():
            giua = self.kiem_tra_diem(ent_giua.get().strip())
            cuoi = self.kiem_tra_diem(ent_cuoi.get().strip())

            if giua is None or cuoi is None:
                messagebox.showwarning("Lỗi", "Điểm phải là số từ 0 đến 10!")
                return

            tb = self.tinh_tb(giua, cuoi)
            diem_dict = self.doc_diem()
            diem_dict[ma_hs] = {
                "giua_ky": str(giua),
                "cuoi_ky": str(cuoi),
                "tb_ca_nam": str(tb),
            }
            self.ghi_diem_file(diem_dict)

            self.view.status_label.config(text=f"Đã lưu điểm cho {ho_ten}")
            messagebox.showinfo("Thành công", f"Đã lưu điểm!\nTB cả năm: {tb}")
            pop.destroy()
            self.tai_du_lieu()

        pop.bind("<Return>", lambda e: luu_diem())
        tk.Button(pop, text="Lưu điểm", bg=self.color_navy, fg="white", font=("Arial", 10, "bold"),
                  command=luu_diem, pady=8, padx=20).pack(pady=10)