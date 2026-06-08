import tkinter as tk
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

        # Sử dụng Model Query tập trung
        self.query = Query()
        self.hs_path = "hocsinh.csv"
        self.diem_path = "diemso.csv"

        self.view = DiemSoView(self.parent, self)
        self.tai_du_lieu()

        self.loading_screen = LoadingScreen(self.parent)  # Khởi tạo
        self.tai_du_lieu_async()  # Dùng hàm async thay cho hàm cũ


    def tai_du_lieu_async(self):
        """Hàm gọi để load dữ liệu không bị treo"""
        self.loading_screen.show()
        threading.Thread(target=self._xu_ly_tai_du_lieu, daemon=True).start()

    def _xu_ly_tai_du_lieu(self):
        """Xử lý đọc dữ liệu ở luồng phụ"""
        df_hs = self.query.read_csv(self.hs_path)
        df_diem = self.query.read_csv(self.diem_path)

        if df_hs.empty:
            self.parent.after(0, self.loading_screen.hide)
            return

        if not df_diem.empty:
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")
        else:
            df_full = df_hs
            df_full[['giua_ky', 'cuoi_ky', 'tb_ca_nam']] = ""

        # Gửi dữ liệu về luồng chính để vẽ
        self.parent.after(0, lambda: self._hoan_thanh_tai_du_lieu(df_full))

    def _hoan_thanh_tai_du_lieu(self, df_full):
        """Vẽ dữ liệu lên Treeview một cách an toàn"""
        # Kiểm tra xem view và treeview còn tồn tại không
        if hasattr(self, 'view') and hasattr(self.view, 'tree') and self.view.tree.winfo_exists():
            # Xóa dữ liệu cũ
            for item in self.view.tree.get_children():
                self.view.tree.delete(item)

            # Nạp dữ liệu mới
            for _, row in df_full.fillna("").iterrows():
                self.view.tree.insert("", "end", values=(
                    row.get('stt', ''), row.get('ho_ten', ''), row.get('ma_hs', ''),
                    row.get('lop', ''), row.get('giua_ky', ''),
                    row.get('cuoi_ky', ''), row.get('tb_ca_nam', '')
                ))

            # Tắt loading nếu view còn tồn tại
            if hasattr(self, 'loading_screen'):
                self.loading_screen.hide()
        else:
            # View đã bị đóng, không làm gì cả để tránh lỗi TclError
            return

    def tinh_tb(self):
        """Tính toán điểm TB bằng Threading để tránh treo ứng dụng"""
        # 1. Bật loading lên
        self.loading_screen.show()

        # 2. Đưa tác vụ nặng vào Thread
        threading.Thread(target=self._xu_ly_tinh_tb_ngam, daemon=True).start()

    def _xu_ly_tinh_tb_ngam(self):
        """Hàm chạy ngầm để tính toán (Worker Thread)"""
        df = self.query.read_csv(self.diem_path)

        if not df.empty:
            # Tính toán
            df['tb_ca_nam'] = (df['giua_ky'] + (df['cuoi_ky'] * 2)) / 3
            df['tb_ca_nam'] = np.round(df['tb_ca_nam'], 1)

            # Lưu file
            self.query.save_csv(df, self.diem_path)

        # 3. Sau khi tính xong, gọi load lại dữ liệu trên Main Thread
        # Lưu ý: Gọi hàm tải dữ liệu async để nó hiện loading tiếp đến khi xong
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

    # Trong lớp DiemSoController:
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

        # Chỉ cần 1 dòng gọi class Popup
        DiemPopup(self.parent, self, student_info)


    def export_data(self):
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not path: return

        self.loading_screen.show()

        def _task_export():
            # Đọc và merge dữ liệu (Công việc nặng)
            df_hs = self.query.read_csv(self.hs_path)
            df_diem = self.query.read_csv(self.diem_path)
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left")

            # Ghi file Excel
            df_full.to_excel(path, index=False)

            # Thông báo thành công và tắt loading
            self.parent.after(0, lambda: [self.loading_screen.hide(),
                                          messagebox.showinfo("Thành công", "Đã xuất bảng điểm!")])

        threading.Thread(target=_task_export, daemon=True).start()

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not path: return

        self.loading_screen.show()

        def _task_import():
            try:
                # Đọc file Excel (Công việc nặng - OK để ở thread này)
                df = pd.read_excel(path)
                self.query.save_csv(df, self.diem_path)

                # DÙNG .after() để đưa các hành động UI về Main Thread
                self.parent.after(0, lambda: self.loading_screen.hide())
                self.parent.after(0, self.tai_du_lieu_async)
                self.parent.after(0, lambda: messagebox.showinfo("Thành công", "Đã nhập bảng điểm!"))

            except Exception as e:
                # Nếu lỗi, cũng phải đưa thông báo về Main Thread
                self.parent.after(0, lambda: self.loading_screen.hide())
                self.parent.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể nhập file: {e}"))

        threading.Thread(target=_task_import, daemon=True).start()

    def tim_kiem(self):
        """Lọc dữ liệu theo Tên, Mã HS hoặc Lớp"""
        tu_khoa = self.view.search_entry.get().lower()

        # 1. Đọc và merge dữ liệu
        df_hs = self.query.read_csv(self.hs_path)
        df_diem = self.query.read_csv(self.diem_path)

        if not df_diem.empty:
            df_full = pd.merge(df_hs, df_diem, on="ma_hs", how="left").fillna("")
        else:
            df_full = df_hs.fillna("")

        # 2. Lọc dữ liệu
        df_ket_qua = df_full[
            df_full['ho_ten'].astype(str).str.lower().str.contains(tu_khoa) |
            df_full['ma_hs'].astype(str).str.lower().str.contains(tu_khoa) |
            df_full['lop'].astype(str).str.lower().str.contains(tu_khoa)
            ]

        # 3. Sử dụng .after để đảm bảo an toàn luồng
        self.parent.after(0, lambda: self._hoan_thanh_tai_du_lieu(df_ket_qua))