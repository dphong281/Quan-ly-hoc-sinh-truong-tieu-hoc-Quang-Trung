import tkinter as tk
import csv
from os import name

from tkinter import messagebox

from Sanpham.common.gd_caidat import CaiDatView  # Import file giao diện tĩnh vừa tạo


class CaiDatPage(tk.Frame):
    def __init__(self, parent,username):
        super().__init__(parent)

        # 1. Khởi tạo giao diện tĩnh từ file gd_caidat
        self.view = CaiDatView(self, username)

        # 2. Gán sự kiện logic (Đúng phong cách tường minh của bạn)
        self.gan_su_kien_giao_dien()

        self.file_path = "database/tk.csv"
        self.username = username


    def gan_su_kien_giao_dien(self):
        # Khi bấm nút Hệ thống -> Gọi hàm mo_tab_he_thong
        self.view.menu_buttons["Hệ thống"].config(command=self.tab_he_thong)

        # Khi bấm nút Bảo mật -> Gọi hàm mo_tab_bao_mat
        self.view.menu_buttons["Bảo mật"].config(command=self.tab_bao_mat)

        #cac nut trong cai dat
        self.view.btn_save.config(command=self.luu_thong_tin)
        self.view.btn_change.config(command=self.doi_mat_khau)



    # Viết thêm 2 hàm xử lý ẩn hiện này vào file logic:
    def tab_he_thong(self):
        self.view.khung_bao_mat.pack_forget()  # Ẩn khung bảo mật bên giao diện tĩnh
        self.view.khung_he_thong.pack(fill="both", expand=True)  # Hiện khung hệ thống bên giao diện tĩnh

    def tab_bao_mat(self):
        self.view.khung_he_thong.pack_forget()  # Ẩn khung hệ thống bên giao diện tĩnh
        self.view.khung_bao_mat.pack(fill="both", expand=True)  # Hiện khung bảo mật bên giao diện tĩnh

    def luu_thong_tin(self):
        ho_ten = self.view.ent_ho_ten.get().strip()
        email = self.view.ent_email.get().strip()
        sdt = self.view.ent_sdt.get().strip()

        if ho_ten == "" or email == "" or sdt == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        rows = []
        user_ton_tai = False

        # Đọc file csv cũ để tìm đúng dòng của user đang đăng nhập
        file_doc = open(self.file_path, "r", encoding="utf-8")
        reader = csv.reader(file_doc)
        for row in reader:
            if row and len(row) >= 2:
                if row[0] == self.username:
                    password = row[1]  # Giữ nguyên mật khẩu cũ
                    # Nối thêm thông tin người dùng vừa nhập vào phía sau tài khoản, mật khẩu
                    row = [self.username, password, name, email, sdt]
                    user_ton_tai = True
                rows.append(row)
        file_doc.close()


        # Ghi đè lại toàn bộ dữ liệu (Dòng của bạn sẽ tự động có thêm họ tên, email, sdt)
        file_ghi = open(self.file_path, "w", newline="", encoding="utf-8")
        writer = csv.writer(file_ghi)
        writer.writerows(rows)
        file_ghi.close()

        messagebox.showinfo("Thành công", "Đã lưu thông tin cá nhân!")



    # --- LOGIC XỬ LÝ 2: ĐỔI MẬT KHẨU ---
    def doi_mat_khau(self):
        # Lấy dữ liệu mật khẩu
        mk_cu = self.view.ent_pass.get().strip()
        mk_moi = self.view.ent_newpass.get().strip()
        nhap_lai = self.view.ent_renewpass.get().strip()

        # 1. Kiểm tra trống
        if mk_cu == "" or mk_moi == "" or nhap_lai == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ !")
            return

        # 2. Kiểm tra mật khẩu mới và Nhập lại có khớp nhau không
        if mk_moi != nhap_lai:
            messagebox.showerror("Lỗi", "Mật khẩu mới và Nhập lại mật khẩu mới không trùng khớp!")
            return

        # 3. Kiểm tra mật khẩu mới trùng mật khẩu cũ
        if mk_cu == mk_moi:
            messagebox.showwarning("Cảnh báo", "Mật khẩu mới không được giống mật khẩu cũ!")
            return

        rows = []  # Danh sách tạm để chứa toàn bộ dữ liệu file csv
        check_pass_dung = False

        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Nếu dòng không bị rỗng
                    # row[0] là Tài khoản, row[1] là Mật khẩu
                    if row[0] == self.username and row[1] == mk_cu:
                        row[1] = mk_moi  # Đổi mật khẩu cũ thành mật khẩu mới trong danh sách tạm
                        check_pass_dung = True
                    rows.append(row)

        # Nếu quét hết file mà không thấy mật khẩu cũ trùng khớp
        if check_pass_dung == False:
            messagebox.showerror("Lỗi", "Mật khẩu hiện tại không chính xác!")
            return

        # 4. Ghi đè lại toàn bộ dữ liệu mới vào file tk.csv
        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)  # Ghi lại toàn bộ danh sách đã sửa mật khẩu công khai

        # Xóa sạch chữ trên các ô nhập sau khi đổi thành công để bảo mật
        self.view.ent_pass.delete(0, tk.END)
        self.view.ent_newpass.delete(0, tk.END)
        self.view.ent_renewpass.delete(0, tk.END)

        messagebox.showinfo("Thành công", "Thay đổi mật khẩu thành công!")
