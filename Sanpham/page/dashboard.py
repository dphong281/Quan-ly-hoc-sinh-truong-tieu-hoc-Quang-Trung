import tkinter as tk
import csv
import os
from tkinter import messagebox

from Sanpham.common.gd_dashboard import DashboardView
from Sanpham.page.danhgia import DanhGiaView
from Sanpham.page.taichinh import TaiChinh
from Sanpham.page.qlhs import QLHSController
from Sanpham.page.caidat import CaiDatPage


class DashboardPage:
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager

        self.view = DashboardView(master, username)
        self.su_kien_giao_dien()
        self.trang_chu()


    # CHUYỂN TRANG
    def su_kien_giao_dien(self):
        buttons = self.view.menu_buttons

        buttons["Trang Chủ"].config(command=self.trang_chu)
        buttons["Học Sinh"].config(command=self.hoc_sinh)
        buttons["Tài Chính"].config(command=self.tai_chinh)
        buttons["Đánh Giá"].config(command=self.danh_gia)
        buttons["Cài Đặt"].config(command=self.cai_dat)
        self.view.btn_logout.config(command=self.logout)


    def clear(self):
        for widget in self.view.change.winfo_children():
            widget.destroy()

    def trang_chu(self):
        self.clear()
        self.view.khung_trang_chu()

        # LOGIC: Đếm số lượng học sinh thực tế từ cơ sở dữ liệu CSV
        tong_hs = 0
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")


        with open(db_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                tong_hs = len(list(reader)) - 1


        data_thong_ke = [
            ("Tổng học sinh", f"{tong_hs}", "#4C51BF", "👥"),
            ("Học sinh mới", "25", "#48BB78", "📈"),
            ("Tổng giáo viên", "85", "#ECC94B", "👨‍🏫")
        ]
        self.view.the_thong_ke(data_thong_ke)

        self.view.the_bieu_do(["Phân loại học sinh", "Tình hình vắng học"])

        ds_lich = [
            ("Lớp Học Kỳ 1 - 1A1", "09:00 - 13:00"),
            ("Lớp Học Kỳ 2 - 2A2", "13:00 - 15:00")
        ]
        ds_tin = [
            "Thông báo nghỉ lễ 30/4 - 1/5",
            "Lịch thi học kỳ mới nhất",
            "Hợp tác đào tạo quốc tế"
        ]
        self.view.lich_va_thong_bao(ds_lich, ds_tin)

        ds_vinh_danh = [
            ("Nguyễn Thị B", "1A1", "9.8"),
            ("Trần Văn C", "1B2", "9.7"),
            ("Lê Hoàng D", "1C3", "9.6"),
            ("Phạm Minh E", "2A2", "9.5")
        ]
        # Gọi view hiển thị vinh danh (View đã tự tích hợp hiệu ứng hover bên trong)
        self.view.vinh_danh(ds_vinh_danh)


    # PAGE QLHS
    def hoc_sinh(self):
        self.clear()
        QLHSController(self.view.change)

    # ĐÁNH GIÁ
    def danh_gia(self):
        self.clear()
        DanhGiaView(self.view.change)

    #PAGE TÀI CHÍNH
    def tai_chinh(self):
        self.clear()
        trang_tc = TaiChinh(self.view.change)
        trang_tc.pack(fill="both", expand=True)

    # NÚT LOGOUT
    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            if hasattr(self.app_manager, 'show_login'):
                self.app_manager.show_login()

    # PAGE SETTING
    def cai_dat(self):
        self.clear()
        trang_cd = CaiDatPage(self.view.change, self.view.username)
        trang_cd.pack(fill="both", expand=True)