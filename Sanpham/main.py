import tkinter as tk
from Sanpham.page.login import LoginPage
from Sanpham.page.dashboard import DashboardPage


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")

        self.current_page = None

        self.show_login()

    def clear(self):
        if self.current_page:
            self.current_page.destroy()

    def show_login(self):
        self.clear()

        self.current_page = tk.Frame(self.root)
        self.current_page.pack(fill="both", expand=True)

        LoginPage(self.current_page, self)

    def show_dashboard(self, username):
        self.clear()

        self.current_page = tk.Frame(self.root)
        self.current_page.pack(fill="both", expand=True)

        DashboardPage(self.current_page, self, username)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý học sinh")
    app = App(root)
    root.mainloop()