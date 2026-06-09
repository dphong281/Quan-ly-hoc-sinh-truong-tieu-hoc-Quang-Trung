import threading
import csv
import os
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Sanpham.model.query import Query
from Sanpham.common.gd_dashboard import DashboardView
from Sanpham.page.danhgia import DanhGiaView
from Sanpham.page.giaovien import GV_Controller
from Sanpham.page.taichinh import TaiChinh
from Sanpham.page.qlhs import QLHSController
from Sanpham.page.diemso import DiemSoController
from Sanpham.page.caidat import CaiDatPage
from Sanpham.assets.loading import LoadingScreen

class DashboardPage:
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager
        self.view = DashboardView(master, username)

        self.view.btn_guide.configure(command=self.mo_huong_dan_pdf)
        self.loading = LoadingScreen(master)

        self.su_kien_giao_dien()
        self.trang_chu()

    def su_kien_giao_dien(self):
        buttons = self.view.menu_buttons
        buttons["Trang Chủ"].configure(command=self.trang_chu)
        buttons["Học Sinh"].configure(command=self.hoc_sinh)
        buttons["Điểm Số"].configure(command=self.diem_so)
        buttons["Giáo Viên"].configure(command=self.giao_vien)
        buttons["Tài Chính"].configure(command=self.tai_chinh)
        buttons["Đánh Giá"].configure(command=self.danh_gia)
        buttons["Cài Đặt"].configure(command=self.cai_dat)
        self.view.btn_logout.configure(command=self.logout)

    def clear(self):
        for widget in self.view.change.winfo_children():
            widget.destroy()

    def lay_hoc_sinh_xuat_sac(self, top=4):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database")
        hs_path = os.path.join(db_path, "hocsinh.csv")
        diem_path = os.path.join(db_path, "diemso.csv")
        diem_dict = {}
        if os.path.exists(diem_path):
            with open(diem_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ma = (row.get("ma_hs") or "").strip()
                    if ma: diem_dict[ma] = (row.get("tb_ca_nam") or "").strip()
        ds_xep_hang = []
        if os.path.exists(hs_path):
            with open(hs_path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ma_hs = row.get("ma_hs", "").strip()
                    ho_ten = row.get("ho_ten", "").strip()
                    lop = row.get("lop", "").strip()
                    tb_raw = diem_dict.get(ma_hs, "0")
                    try:
                        diem_so = float(tb_raw.replace(",", "."))
                        ds_xep_hang.append((ho_ten, lop, tb_raw, diem_so))
                    except: continue
        ds_xep_hang.sort(key=lambda x: x[3], reverse=True)
        return [(ten, lop, diem) for ten, lop, diem, _ in ds_xep_hang[:top]]

    def trang_chu(self):
        self.clear()
        self.view.khung_trang_chu()
        query = Query()
        tong_hs = len(query.get_all("hocsinh.csv"))
        tong_gv = len(query.get_all("giaovien.csv"))
        self.view.the_thong_ke([("Tổng học sinh", f"{tong_hs}", "#4C51BF", ""), ("Giáo viên", f"{tong_gv}", "#48BB78", "")])
        self.view.the_bieu_do()
        self.ve_bieu_do()
        self.view.lich_va_thong_bao([("Lớp 1A1", "09:00"), ("Lớp 2A2", "13:00")], ["Thông báo nghỉ lễ", "Lịch thi học kỳ"])
        self.view.vinh_danh(self.lay_hoc_sinh_xuat_sac())

    def ve_bieu_do(self):
        try:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "database", "hocsinh.csv")
            fig, ax = plt.subplots(figsize=(5, 2.5), dpi=100)
            df = pd.read_csv(db_path)
            df['lop'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#0d62b8')
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.view.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        except Exception as e:
            print(f"Lỗi vẽ biểu đồ: {e}")

    def hoc_sinh(self):
        self.clear()
        QLHSController(self.view.change)

    def giao_vien(self):
        self.clear()
        GV_Controller(self.view.change)

    def tai_chinh(self):
        self.clear()
        trang_tc = TaiChinh(self.view.change)
        trang_tc.pack(fill="both", expand=True)

    def cai_dat(self):
        self.clear()
        CaiDatPage(self.view.change, self.view.username)

    def diem_so(self):
        self.clear()
        DiemSoController(self.view.change)

    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            self.app_manager.show_login()

    import os
    from tkinter import messagebox

    def mo_huong_dan_pdf(self):
        # 1. Lấy đường dẫn của file dashboard.py hiện tại
        current_file = os.path.abspath(__file__)  # D:\python\Quan-ly... \dashboard.py

        # 2. Tìm đường dẫn tới thư mục 'Sanpham'
        # Chúng ta tìm chuỗi 'Sanpham' trong đường dẫn
        base_dir = current_file.split('Sanpham')[0] + 'Sanpham'

        # 3. Kết hợp để ra đường dẫn file PDF: Sanpham/assets/Huong_dan.pdf
        path_pdf = os.path.join(base_dir, "assets", "Huong_dan.pdf")

        # Kiểm tra
        if not os.path.exists(path_pdf):
            messagebox.showerror("Lỗi", f"Không tìm thấy file tại:\n{path_pdf}")
            return

        try:
            os.startfile(path_pdf)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {e}")

    def danh_gia(self):
        self.clear()


        DanhGiaView(self.view.change, self.app_manager)