import customtkinter as ctk
from Sanpham.common.gd_login import LoginView
from Sanpham.page.dashboard import DashboardPage

# Cấu hình giao diện tổng thể
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Học sinh")
        self.root.geometry("1200x700")

        self.current_page = None
        self.show_login()

    def clear(self):
        if self.current_page:
            self.current_page.destroy()

    def show_login(self):
        self.clear()

        self.current_page = ctk.CTkFrame(self.root, fg_color="#D1E9F6")
        self.current_page.pack(fill="both", expand=True)

        LoginView(self.current_page, self)

    def show_dashboard(self, username):
        self.clear()

        self.current_page = ctk.CTkFrame(self.root, fg_color="#F5F5F5")
        self.current_page.pack(fill="both", expand=True)

        DashboardPage(self.current_page, self, username)

if __name__ == "__main__":
    root = ctk.CTk()
    app_manager = App(root)
    root.mainloop()
