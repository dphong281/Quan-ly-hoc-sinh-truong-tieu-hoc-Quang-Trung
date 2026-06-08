import customtkinter as ctk
from PIL import Image


class DashboardView:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.configure(fg_color="#ebebeb")

        # Cấu hình grid tổng thể: Cột 0 (sidebar), Cột 1 (nội dung)
        # Hàng 0 chiếm toàn bộ chiều dọc
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.gd_sidebar()
        self.gd_main_content()
        self.mc_header()
        self.mc_body()

    def gd_sidebar(self):
        # Sử dụng grid với sticky="nsew" để phủ kín chiều dọc
        self.sidebar = ctk.CTkFrame(self.master, fg_color="#0d62b8", width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.pack_propagate(False)

        try:
            img_side = Image.open("assets/logo.png")
            self.photo_side = ctk.CTkImage(light_image=img_side, dark_image=img_side, size=(190, 120))
            ctk.CTkLabel(self.sidebar, image=self.photo_side, text="", fg_color="#0d62b8").pack(pady=25)
        except:
            ctk.CTkLabel(self.sidebar, text="LOGO SCHOOL", text_color="white", fg_color="#0d62b8",
                         font=("Arial", 16, "bold")).pack(pady=40)

        self.menu_buttons = {}
        for item in ["Trang Chủ", "Học Sinh", "Điểm Số", "Giáo Viên", "Tài Chính", "Đánh Giá", "Cài Đặt"]:
            btn = ctk.CTkButton(self.sidebar, text=f"  {item}", font=("Arial", 12, "bold"),
                                fg_color="#0d62b8", hover_color="#0a4d91", text_color="white",
                                corner_radius=0, anchor="w", height=40)
            btn.pack(fill="x", pady=2, padx=10)
            self.menu_buttons[item] = btn

        self.btn_logout = ctk.CTkButton(self.sidebar, text="  Đăng xuất", fg_color="#0d62b8",
                                        hover_color="#9B2C2C", text_color="#FEB2B2", font=("Arial", 11, "bold"),
                                        corner_radius=0, anchor="w", height=40)
        self.btn_logout.pack(side="bottom", fill="x", pady=20, padx=10)

    def gd_main_content(self):
        # Khu vực nội dung chính nằm ở cột 1, giãn theo cửa sổ
        self.main_area = ctk.CTkFrame(self.master, fg_color="#ebebeb", corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # Cấu hình grid cho main_area: Header ở hàng 0, Body ở hàng 1
        self.main_area.grid_rowconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

    def mc_header(self):
        self.header = ctk.CTkFrame(self.main_area, fg_color="white", height=60, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")  # Giãn ngang
        self.header.pack_propagate(False)

        ctk.CTkLabel(self.header, text=f"Chào mừng, {self.username}!", text_color="#2D3748",
                     font=("Arial", 14, "bold")).pack(side="left", padx=20)

        self.btn_guide = ctk.CTkButton(self.header, text="📖 Hướng dẫn", width=120, height=30,
                                       fg_color="#65C1D9", hover_color="#52A9C1", text_color="white")
        self.btn_guide.pack(side="right", padx=20)

    def mc_body(self):
        # Body nằm ở hàng 1, sticky="nsew" để phủ kín không gian còn lại
        self.change = ctk.CTkFrame(self.main_area, fg_color="#ebebeb", corner_radius=0)
        self.change.grid(row=1, column=0, sticky="nsew")

    def khung_trang_chu(self):
        for widget in self.change.winfo_children(): widget.destroy()
        self.noidung = ctk.CTkFrame(self.change, fg_color="#ebebeb", corner_radius=0)
        self.noidung.pack(fill="both", expand=True, padx=30, pady=20)

        # Cấu hình grid cho noidung
        self.noidung.grid_columnconfigure(0, weight=7)
        self.noidung.grid_columnconfigure(1, weight=3)

        self.phan_trai = ctk.CTkFrame(self.noidung, fg_color="#ebebeb", corner_radius=0)
        self.phan_trai.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Cấu hình grid cho phan_trai để các ô con xếp hàng dọc đều nhau
        self.phan_trai.grid_columnconfigure(0, weight=1)

        self.phan_phai = ctk.CTkFrame(self.noidung, fg_color="white", corner_radius=10, border_width=1,
                                      border_color="#E2E8F0")
        self.phan_phai.grid(row=0, column=1, sticky="nsew")

    def the_thong_ke(self, data_list):
        the_1 = ctk.CTkFrame(self.phan_trai, fg_color="#ebebeb", corner_radius=0)
        the_1.pack(fill="x", pady=(0, 20))

        for i, (title, value, color, icon) in enumerate(data_list):
            card = ctk.CTkFrame(the_1, fg_color="white", corner_radius=8, border_width=1, border_color="#E2E8F0")
            card.pack(side="left", fill="x", expand=True, padx=(0, 15 if i < len(data_list) - 1 else 0))

            # Khung chứa text để căn giữa
            ctk.CTkFrame(card, fg_color=color, height=4, corner_radius=0).pack(side="bottom", fill="x")

            # Dùng anchor="center" để căn giữa theo chiều ngang
            ctk.CTkLabel(card, text=title, fg_color="white", text_color="#718096",
                         font=("Arial", 9, "bold")).pack(pady=(15, 0), anchor="center")

            ctk.CTkLabel(card, text=value, fg_color="white", text_color="#2D3748",
                         font=("Arial", 18, "bold")).pack(pady=(0, 15), anchor="center")

    def the_bieu_do(self):
        self.bieu_do_frame = ctk.CTkFrame(self.phan_trai, fg_color="white", corner_radius=8, border_width=1,
                                          border_color="#E2E8F0")
        self.bieu_do_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(self.bieu_do_frame, text="Thống kê sĩ số theo lớp", fg_color="white", text_color="#2D3748",
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=10)
        self.canvas_frame = ctk.CTkFrame(self.bieu_do_frame, fg_color="white", corner_radius=0)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def lich_va_thong_bao(self, ds_lich, ds_tin):
        the_3 = ctk.CTkFrame(self.phan_trai, fg_color="#ebebeb", corner_radius=0)
        the_3.pack(fill="both", expand=True)
        lich_frame = ctk.CTkFrame(the_3, fg_color="white", corner_radius=8, border_width=1, border_color="#E2E8F0")
        lich_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        ctk.CTkLabel(lich_frame, text="Lịch biểu hôm nay", fg_color="white", text_color="#2D3748",
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
        for ten, gio in ds_lich:
            row = ctk.CTkFrame(lich_frame, fg_color="white")
            row.pack(fill="x", padx=15, pady=5)
            ctk.CTkLabel(row, text=f"• {ten}", fg_color="white", font=("Arial", 9)).pack(side="left")
            ctk.CTkLabel(row, text=gio, fg_color="white", text_color="#718096", font=("Arial", 8)).pack(side="right")
        tb_frame = ctk.CTkFrame(the_3, fg_color="white", corner_radius=8, border_width=1, border_color="#E2E8F0")
        tb_frame.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(tb_frame, text="Thông báo gần đây", fg_color="white", text_color="#2D3748",
                     font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
        for tin in ds_tin:
            ctk.CTkLabel(tb_frame, text=f" • {tin}", fg_color="white", text_color="#4A5568", font=("Arial", 9),
                         anchor="w").pack(fill="x", padx=15, pady=4)

    def vinh_danh(self, ds_vinh_danh):
        ctk.CTkLabel(self.phan_phai, text="Học sinh xuất sắc nhất tháng", fg_color="white", text_color="#2D3748",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=20)
        for ten, lop, diem in ds_vinh_danh:
            item = ctk.CTkFrame(self.phan_phai, fg_color="white")
            item.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(item, text="👤", font=("Arial", 14), fg_color="#EDF2F7", width=30, height=30,
                         corner_radius=5).pack(side="left")
            info = ctk.CTkFrame(item, fg_color="white")
            info.pack(side="left", padx=10)
            ctk.CTkLabel(info, text=ten, fg_color="white", font=("Arial", 9, "bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=lop, fg_color="white", text_color="#718096", font=("Arial", 8)).pack(anchor="w")
            ctk.CTkLabel(item, text=diem, fg_color="white", text_color="#48BB78", font=("Arial", 10, "bold")).pack(
                side="right")