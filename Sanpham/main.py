import tkinter as tk
from Sanpham.common.gd_login import LoginPage
from Sanpham.common.gd_dashboard import DashboardPage


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Học sinh")
        self.root.geometry("1000x600")

        self.current_page = None
        self.show_login()

    def clear(self):
        if self.current_page:
            self.current_page.destroy()

    def show_login(self):
        self.clear()

        self.root.configure(bg="#D1E9F6") #nền app

        #frame login
        self.current_page = tk.Frame(self.root, bg="#D1E9F6")
        self.current_page.pack(fill="both", expand=True)


        LoginPage(self.current_page, self)


    def show_dashboard(self, username):
        self.clear()

        self.root.configure(bg="#F5F5F5")

        self.current_page = tk.Frame(self.root, bg="#F5F5F5")
        self.current_page.pack(fill="both", expand=True)

        DashboardPage(self.current_page, self, username)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()