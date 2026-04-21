import tkinter as tk
from page.login import LoginPage
from page.quanlyhs import QuanLyHSPage
from page.themhs import ThemHSPage
from page.suahs import SuaHSPage

"lớp chính"
class AppManager:
    def __init__(self):    #"hàm khởi tạo"
        self.root = tk.Tk()   #"self = AppManager"  #"root = để vẽ giao diện"
        self.root.title("Quản lý học sinh - Tiểu học Quang Trung")
        self.root.geometry("300x200")
        self.current_page = None      #"lưu page hiện tại"
        self.show_login_page()        #"mở app sẽ vào trang login"

    "Xóa tất cả widget của page hiện tại"
    def clear_current_page(self):
        if self.current_page:
            for widget in self.root.winfo_children():   #"lặp qua tất cả widget trong page"
                widget.destroy()     #"chuyển trang -> xóa toàn bộ page cũ"

    "Hiển thị trang đăng nhập"
    def show_login_page(self):
        self.clear_current_page()
        self.root.geometry("300x200")
        self.current_page = LoginPage(self.root, self)
        "LoginPage() = tạo 1 trang login"
        "(.....) = truyền dữ liệu vào tràn"
        " self.current_page = lưu trang hiện tại "

    "Hiển thị trang QL hs"
    def show_quanlyhs_page(self):
        self.clear_current_page()
        self.root.geometry("600x400")
        self.current_page = QuanLyHSPage(self.root, self)

    "Hiển thị trang thêm thông tin hs"
    def show_themhs_page(self):
        self.clear_current_page()
        self.root.geometry("400x300")
        self.current_page = ThemHSPage(self.root, self)

    "Hiển thị trang sửa thông tin hs"
    def show_suahs_page(self, index):
        self.clear_current_page()
        self.root.geometry("400x300")
        self.current_page = SuaHSPage(self.root, self, index)

    "chạy ứng dụng"
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppManager()
    app.run()