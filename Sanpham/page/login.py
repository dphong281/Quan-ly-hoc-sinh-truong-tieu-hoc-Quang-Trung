import tkinter as tk
from tkinter import messagebox

def kiem_tra_dang_nhap(u, p, app_manager):

    # HÀM ĐỌC FILE
    with open("database/tk.csv", "r") as file:
        for line in file:
            tk_info = line.strip().split(",")

            # VÒNG LẶP KIỂM TRA U & P
            if len(tk_info) >= 2 and u == tk_info[0] and p == tk_info[1]:
                messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
                app_manager.show_dashboard(u)
                return True

        messagebox.showerror("Thông báo", "Sai tài khoản hoặc mật khẩu")
        return False