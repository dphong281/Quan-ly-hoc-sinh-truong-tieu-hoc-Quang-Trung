import tkinter as tk
import csv
from tkinter import messagebox

from Sanpham.common.gd_caidat import CaiDatView


class CaiDatPage(tk.Frame):
    def __init__(self, parent, username):

        self.view = CaiDatView(parent, username)

        self.gan_su_kien_giao_dien()

        self.file_path = "database/tk.csv"
        self.username = username


    def gan_su_kien_giao_dien(self):
        self.view.menu_buttons["Hệ thống"].configure(command=self.tab_he_thong)
        self.view.menu_buttons["Bảo mật"].configure(command=self.tab_bao_mat)
        self.view.menu_buttons["Giới thiệu"].configure(command=self.tab_about)

        self.view.btn_save.configure(command=self.luu_thong_tin)
        self.view.btn_change.configure(command=self.doi_mat_khau)

    def tab_he_thong(self):
        self.view.khung_he_thong.tkraise()
    def tab_bao_mat(self):
        self.view.khung_bao_mat.tkraise()
    def tab_about(self):
        self.view.khung_about.tkraise()

    def luu_thong_tin(self):
        ho_ten = self.view.ent_ho_ten.get().strip()
        email = self.view.ent_email.get().strip()
        sdt = self.view.ent_sdt.get().strip()

        if ho_ten == "" or email == "" or sdt == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        rows = []
        user_ton_tai = False

        file_doc = open(self.file_path, "r", encoding="utf-8")
        reader = csv.reader(file_doc)
        for row in reader:
            if row and len(row) >= 2:
                if row[0] == self.username:
                    password = row[1]

                    row = [self.username, password, ho_ten, email, sdt]
                    user_ton_tai = True
                rows.append(row)
        file_doc.close()

        if user_ton_tai == False:
            messagebox.showerror("Lỗi", "Tài khoản không tồn tại !")
            return

        file_ghi = open(self.file_path, "w", newline="", encoding="utf-8")
        writer = csv.writer(file_ghi)
        writer.writerows(rows)
        file_ghi.close()

        messagebox.showinfo("Thành công", "Đã lưu thông tin cá nhân!")


    def doi_mat_khau(self):
        mk_cu = self.view.ent_pass.get().strip()
        mk_moi = self.view.ent_newpass.get().strip()
        nhap_lai = self.view.ent_renewpass.get().strip()

        if mk_cu == "" or mk_moi == "" or nhap_lai == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ !")
            return

        if mk_moi != nhap_lai:
            messagebox.showerror("Lỗi", "Mật khẩu mới và Nhập lại mật khẩu mới không trùng khớp!")
            return

        if mk_cu == mk_moi:
            messagebox.showwarning("Cảnh báo", "Mật khẩu mới không được giống mật khẩu cũ!")
            return

        rows = []
        check_pass_dung = False

        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    if row[0] == self.username and row[1] == mk_cu:
                        row[1] = mk_moi
                        check_pass_dung = True
                    rows.append(row)

        if check_pass_dung == False:
            messagebox.showerror("Lỗi", "Mật khẩu hiện tại không chính xác!")
            return

        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self.view.ent_pass.delete(0, tk.END)
        self.view.ent_newpass.delete(0, tk.END)
        self.view.ent_renewpass.delete(0, tk.END)

        messagebox.showinfo("Thành công", "Thay đổi mật khẩu thành công!")