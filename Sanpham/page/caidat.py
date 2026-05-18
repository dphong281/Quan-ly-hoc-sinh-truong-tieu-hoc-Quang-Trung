import tkinter as tk
from tkinter import messagebox
from Sanpham.common.gd_caidat import CaiDatView  # Import file giao diện tĩnh vừa tạo


class CaiDatPage(tk.Frame):
    def __init__(self, parent,username):
        super().__init__(parent)

        # 1. Khởi tạo giao diện tĩnh từ file gd_caidat
        self.view = CaiDatView(self, username)

        # 2. Gán sự kiện logic (Đúng phong cách tường minh của bạn)
        self.gan_su_kien_giao_dien()


    def gan_su_kien_giao_dien(self):
        # Khi bấm nút Hệ thống -> Gọi hàm mo_tab_he_thong
        self.view.menu_buttons["Hệ thống"].config(command=self.tab_he_thong)

        # Khi bấm nút Bảo mật -> Gọi hàm mo_tab_bao_mat
        self.view.menu_buttons["Bảo mật"].config(command=self.tab_bao_mat)

        self.view.menu_buttons["Giao diện"].config(command=self.tab_giao_dien)

    # Viết thêm 2 hàm xử lý ẩn hiện này vào file logic:
    def tab_he_thong(self):
        self.view.khung_bao_mat.pack_forget()  # Ẩn khung bảo mật bên giao diện tĩnh
        self.view.khung_giao_dien.pack_forget()
        self.view.khung_he_thong.pack(fill="both", expand=True)  # Hiện khung hệ thống bên giao diện tĩnh

    def tab_bao_mat(self):
        self.view.khung_he_thong.pack_forget()  # Ẩn khung hệ thống bên giao diện tĩnh
        self.view.khung_giao_dien.pack_forget()
        self.view.khung_bao_mat.pack(fill="both", expand=True)  # Hiện khung bảo mật bên giao diện tĩnh

    def tab_giao_dien(self):
        self.view.khung_he_thong.pack_forget()
        self.view.khung_bao_mat.pack_forget()  # Ẩn khung bảo mật bên giao diện tĩnh
        self.view.khung_giao_dien.pack(fill="both", expand=True)  # Hiện khung hệ thống bên giao diện tĩnh