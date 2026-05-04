import tkinter as tk
from tkinter import messagebox


def kiem_tra_dang_nhap(u, p, app_manager):
        with open("database/tk.csv", "r") as file: # dùng with để tự động đóng file
            for line in file:
                tk_info = line.strip().split(",")

                if len(tk_info) >= 2 and u == tk_info[0] and p == tk_info[1]:                #kiểm tra u và p
                    messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
                    app_manager.show_dashboard(u)
                    return True

            messagebox.showerror("Thông báo", "Sai tài khoản hoặc mật khẩu")
            return False
