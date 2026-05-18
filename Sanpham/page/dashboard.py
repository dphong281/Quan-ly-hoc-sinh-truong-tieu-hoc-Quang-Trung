import tkinter as tk
import csv
import os

from tkinter import messagebox

from discord.ext.commands import command

from Sanpham.common.ef_dashboard import UIEffects
from Sanpham.common.gd_dashboard import DashboardView
from Sanpham.page.danhgia import DanhGiaView
from Sanpham.page.taichinh import TaiChinh
from Sanpham.page.qlhs import QLHSView
from Sanpham.page.caidat import CaiDatPage


class DashboardPage:
    def __init__(self, master, app_manager, username):
        self.master = master
        self.app_manager = app_manager

        self.view = DashboardView(master, username)

        self.su_kien_giao_dien()

        self.trang_chu()

    def su_kien_giao_dien(self):
        # 1. Lấy danh sách các nút từ giao diện ra cho ngắn gọn
        buttons = self.view.menu_buttons

        # 2. Gán sự kiện chuyển trang trực tiếp cho từng nút
        buttons["Trang Chủ"].config(command=self.trang_chu)
        buttons["Học Sinh"].config(command=self.hoc_sinh)
        buttons["Tài Chính"].config(command=self.tai_chinh)
        buttons["Đánh Giá"].config(command=self.danh_gia)
        buttons["Cài Đặt"].config(command=self.cai_dat)

        # Các nút chưa làm chức năng thì gán vào trang giả lập
        buttons["Điểm Số"].config(command=lambda: self.hien_thi_trang_gia_lap("QUẢN LÝ ĐIỂM SỐ"))

        # Nút đăng xuất
        self.view.btn_logout.config(command=self.logout)


    def xoa_vung_noi_dung(self):
        for widget in self.view.vung_thay_doi.winfo_children():
            widget.destroy()


    def trang_chu(self):

        self.xoa_vung_noi_dung()
        self.view.khung_trang_chu()

        # --- ĐOẠN CODE ĐẾM HỌC SINH SIÊU NGẮN GỌN ---
        tong_hs = 0

        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")

        if os.path.exists(db_path):
            try:
                with open(db_path, mode="r", encoding="utf-8") as f:
                    reader = csv.reader(f)

                    tong_hs = len(list(reader)) - 1

            except Exception as e:
                print(f"Lỗi đọc file: {e}")
        # --------------------------------------------

                # 3. Thẻ thống kê (Thay con số "1,250" cũ bằng biến tong_hs vừa đếm được)
        data_thong_ke = [
            ("Tổng học sinh", f"{tong_hs}", "#4C51BF", "👥"),  # Hiện số thực tế ở đây
            ("Học sinh mới", "25", "#48BB78", "📈"),
            ("Tổng giáo viên", "85", "#ECC94B", "👨‍🏫")
            ]
        self.view.the_thong_ke(data_thong_ke)

        self.view.the_bieu_do(["Phân loại học sinh", "Tình hình vắng học"])

        ds_lich = [
            ("Lớp Học Kỳ 1 - 1A1", "09:00 - 13:00"),
            ("Lớp Học Kỳ 2 - 2A2", "13:00 - 15:00")]
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
        items_vinh_danh = self.view.vinh_danh(ds_vinh_danh)
        for item in items_vinh_danh:
            UIEffects.apply_card_hover(item, normal_bg="white", hover_bg="#F3F4F6")


    def hoc_sinh(self):
        self.xoa_vung_noi_dung()
        if QLHSView is not None:
            try:
                QLHSView(self.view.vung_thay_doi)
            except Exception as e:
                tk.Label(self.view.vung_thay_doi, text=f"Lỗi tải trang: {e}", fg="red").pack(pady=20)
        else:
            self.hien_thi_trang_gia_lap("QUẢN LÝ HỌC SINH")


    def danh_gia(self):
        """Xoá sạch trang cũ và nhét giao diện Đánh giá vào vùng hiển thị chính"""
        self.xoa_vung_noi_dung()
        try:
            DanhGiaView(self.view.vung_thay_doi)
        except Exception as e:
            tk.Label(self.view.vung_thay_doi, text=f"Lỗi tải trang đánh giá: {e}", fg="red").pack(pady=20)


    # 3. THÊM HÀM CHUYỂN SANG TRANG TÀI CHÍNH Ở ĐÂY
    def tai_chinh(self):
        """Xoá sạch trang cũ và nhúng trang Tài Chính vào vùng nội dung chính"""
        self.xoa_vung_noi_dung()
        try:
            # Nhúng trực tiếp class Tài Chính (vốn là một tk.Frame) vào vùng thay đổi nội dung
            trang_tc = TaiChinh(self.view.vung_thay_doi)
            trang_tc.pack(fill="both", expand=True)
        except Exception as e:
            tk.Label(self.view.vung_thay_doi, text=f"Lỗi tải trang tài chính: {e}", fg="red").pack(pady=20)


    def hien_thi_trang_gia_lap(self, tieu_de):
        self.xoa_vung_noi_dung()
        khung = tk.Frame(self.view.vung_thay_doi, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        khung.pack(fill="both", expand=True, padx=30, pady=20)
        tk.Label(khung, text=f" GIAO DIỆN: {tieu_de}", font=("Arial", 18, "bold"), bg="white", fg="#0d62b8").pack(
            expand=True)


    def logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn đăng xuất?"):
            if hasattr(self.app_manager, 'show_login'):
                self.app_manager.show_login()

    def cai_dat(self):
        self.xoa_vung_noi_dung()
        try:
            trang_cd = CaiDatPage(self.view.vung_thay_doi,self.view.username)
            trang_cd.pack(fill="both", expand=True)
        except Exception as e:
            tk.Label(self.view.vung_thay_doi, text=f"Lỗi: {e}", fg="red").pack(pady=20)