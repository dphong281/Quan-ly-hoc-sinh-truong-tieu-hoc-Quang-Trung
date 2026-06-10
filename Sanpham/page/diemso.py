from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
from Sanpham.model.query import Query
from Sanpham.common.gd_diemso import DiemSoView
import threading
from Sanpham.assets.loading import LoadingScreen
from Sanpham.assets.popup_diem import DiemPopup


class DiemSoController:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"

        self.query = Query()
        self.hs_path = "hocsinh.csv"
        self.diem_path = "diemso.csv"

        self.view = DiemSoView(self.parent, self)
        self.tai_du_lieu()

        self.loading_screen = LoadingScreen(self.parent)
        self.tai_du_lieu_async()


    def tai_du_lieu_async(self):
        self.loading_screen.show()
        threading.Thread(target=self._xu_ly_tai_du_lieu, daemon=True).start()

    def _xu_ly_tai_du_lieu(self):
        df_hs = self.query.read_csv(self.hs_path)
        df_diem = self.query.read_csv(self.diem_path)

        ds_ma_hs_diem = df_diem['ma_hs'].astype(str).tolist() if not df_diem.empty else []

        hs_moi = df_hs[~df_hs['ma_hs'].astype(str).isin(ds_ma_hs_diem)]

        if not hs_moi.empty:
            them_vao = pd.DataFrame({
                'ma_hs': hs_moi['ma_hs'],
                'giua_ky': "",
                'cuoi_ky': "",
                'tb_ca_nam': ""
            })
            df_diem = pd.concat([df_diem, them_vao], ignore_index=True)
            self.query.save_csv(df_diem, self.diem_path)

        df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")

        self.parent.after(0, lambda: self._hoan_thanh_tai_du_lieu(df_full))

    def _hoan_thanh_tai_du_lieu(self, df_full):

        if hasattr(self, 'view') and hasattr(self.view, 'tree') and self.view.tree.winfo_exists():
            for item in self.view.tree.get_children():
                self.view.tree.delete(item)

            for _, row in df_full.fillna("").iterrows():
                self.view.tree.insert("", "end", values=(
                    row.get('stt', ''), row.get('ho_ten', ''), row.get('ma_hs', ''),
                    row.get('lop', ''), row.get('giua_ky', ''),
                    row.get('cuoi_ky', ''), row.get('tb_ca_nam', '')
                ))

            if hasattr(self, 'loading_screen'):
                self.loading_screen.hide()
        else:
            return

    def tinh_tb(self):

        self.loading_screen.show()

        threading.Thread(target=self._xu_ly_tinh_tb_ngam, daemon=True).start()

    def _xu_ly_tinh_tb_ngam(self):

        df = self.query.read_csv(self.diem_path)

        if not df.empty:

            df['tb_ca_nam'] = (df['giua_ky'] + (df['cuoi_ky'] * 2)) / 3
            df['tb_ca_nam'] = np.round(df['tb_ca_nam'], 1)

            self.query.save_csv(df, self.diem_path)

        self.parent.after(0, self.tai_du_lieu_async)

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
            messagebox.showwarning("Chọn học sinh", "Vui lòng chọn một học sinh!")
            return

        values = self.view.tree.item(selected[0])["values"]
        student_info = {
            "ho_ten": values[1], "ma_hs": values[2], "lop": values[3],
            "giua_cu": str(values[4]), "cuoi_cu": str(values[5])
        }

        DiemPopup(self.parent, self, student_info)


    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not path: return

        self.loading_screen.show()

        def _task_export():
            # Đọc và merge dữ liệu
            df_hs = self.query.read_csv(self.hs_path)
            df_diem = self.query.read_csv(self.diem_path)
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")

            # Ghi file Excel
            df_full.to_excel(path, index=False)

            # Thông báo và tắt loading
            self.parent.after(0, lambda: [self.loading_screen.hide(),
                                          messagebox.showinfo("Thành công", "Đã xuất bảng điểm!")])

        threading.Thread(target=_task_export, daemon=True).start()

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return

        self.loading_screen.show()

        def _task_import():
            try:
                df = pd.read_excel(path)

                df.columns = df.columns.str.strip()

                if df.empty:
                    raise ValueError("File Excel này không có dữ liệu!")

                required_columns = ['MaSV', 'Diem']
                if not all(col in df.columns for col in required_columns):
                    raise ValueError(f"Lỗi !")

                # Lưu file
                self.query.save_csv(df, self.diem_path)

                #  Cập nhật giao diện
                self.parent.after(0, self.loading_screen.hide)
                self.parent.after(0, self.tai_du_lieu_async)
                self.parent.after(0, messagebox.showinfo, "Thành công", "Đã nhập bảng điểm!")

            except Exception as e:
                # Cấu hình lỗi
                error_msg = f"Không thể nhập file:\n{str(e)}"

                # Cập nhật giao diện
                self.parent.after(0, self.loading_screen.hide)
                self.parent.after(0, messagebox.showerror, "Lỗi nhập liệu", error_msg)

        threading.Thread(target=_task_import, daemon=True).start()

    def tim_kiem(self):
        tu_khoa = self.view.search_entry.get().lower()

        # Đọc và merge dữ liệu
        df_hs = self.query.read_csv(self.hs_path)
        df_diem = self.query.read_csv(self.diem_path)

        if not df_diem.empty:
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left").fillna("")
        else:
            df_full = df_hs.fillna("")

        # Lọc dữ liệu
        df_ket_qua = df_full[
            df_full['ho_ten'].astype(str).str.lower().str.contains(tu_khoa) |
            df_full['ma_hs'].astype(str).str.lower().str.contains(tu_khoa) |
            df_full['lop'].astype(str).str.lower().str.contains(tu_khoa)
            ]

        # Sử dụng .after để đảm bảo an toàn luồng
        self.parent.after(0, lambda: self._hoan_thanh_tai_du_lieu(df_ket_qua))