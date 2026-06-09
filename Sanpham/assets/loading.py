import customtkinter as ctk


class LoadingScreen:
    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(self.master, fg_color="white")

        # Nhãn hiệu ứng
        self.label = ctk.CTkLabel(
            self.frame,
            text=" Đang xử lý dữ liệu...",
            font=("Arial", 20, "bold"),
            text_color="#0d62b8"
        )
        self.label.pack(expand=True)

    def show(self):
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.master.update()

    def hide(self):
        self.frame.place_forget()

    def show_in_frame(self, target_frame):
        self.frame.place(in_=target_frame, relx=0, rely=0, relwidth=1, relheight=1)
        self.master.update()
