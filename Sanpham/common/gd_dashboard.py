import tkinter as tk
from PIL import Image, ImageTk

class DashboardView:
    def __init__(self, master, username):
        self.master = master
        self.username = username

        self.master.configure(bg="#ebebeb")

        self.gd_sidebar()
        self.gd_main_content()
        self.mc_header()
        self.mc_body()

    def gd_sidebar(self):
        self.sidebar = tk.Frame(self.master, bg="#0d62b8", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        try:
            img_side = Image.open("assets/logo.png")
            img_side = img_side.resize((190, 120), Image.LANCZOS)
            self.photo_side = ImageTk.PhotoImage(img_side)
            self.lbl_logo_side = tk.Label(self.sidebar, image=self.photo_side, bg="#0d62b8")
            self.lbl_logo_side.pack(pady=25)
        except:
            tk.Label(self.sidebar, text="LOGO SCHOOL", fg="white", bg="#0d62b8", font=("Arial", 16, "bold")).pack(pady=40)

        # Lưu danh sách các button menu để file Logic có thể gán sự kiện sau
        self.menu_buttons = {}
        menu_items = ["Trang Chủ", "Học Sinh", "Điểm Số", "Tài Chính", "Đánh Giá", "Cài Đặt"]

        for item in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=f"  {item}",
                fg="white",
                bg="#0d62b8",
                font=("Arial", 12, "bold"),
                bd=0,
                anchor="w",
                cursor="hand2",
                activebackground="#0a4d91",
                activeforeground="white"
            )
            btn.pack(fill="x", pady=2, padx=10, ipady=8)
            self.menu_buttons[item] = btn

        self.btn_logout = tk.Button(
            self.sidebar,
            text="  Đăng xuất",
            fg="#FEB2B2",
            bg="#0d62b8",
            font=("Arial", 11, "bold"),
            bd=0, anchor="w",
            cursor="hand2"
        )
        self.btn_logout.pack(side="bottom", fill="x", pady=20, padx=10, ipady=8)

    def gd_main_content(self):
        self.main_area = tk.Frame(self.master, bg="#ebebeb")
        self.main_area.pack(side="right", fill="both", expand=True)

    def mc_header(self):
        self.header = tk.Frame(self.main_area, bg="white", height=70)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        phan_trai = tk.Frame(self.header, bg="white")
        phan_trai.pack(side="left", padx=20, pady=10)

        tk.Label(phan_trai,
                 text=f"Chào mừng, {self.username}!",
                 bg="white",
                 fg="#2D3748",
                 font=("Arial", 14, "bold")).pack(anchor="w")

        phan_phai = tk.Frame(self.header, bg="white")
        phan_phai.pack(side="right", padx=20, fill="y")
        tk.Label(phan_phai, text="👤", bg="white", font=("Arial", 14)).pack(side="left", padx=10)

    def mc_body(self):
        # Khu vực chứa nội dung thay đổi linh hoạt
        self.vung_thay_doi = tk.Frame(self.main_area, bg="#ebebeb")
        self.vung_thay_doi.pack(fill="both", expand=True)

    def khung_trang_chu(self):
        self.noidung = tk.Frame(self.vung_thay_doi, bg="#ebebeb")
        self.noidung.pack(fill="both", expand=True, padx=30, pady=20)
        self.noidung.columnconfigure(0, weight=7)
        self.noidung.columnconfigure(1, weight=3)
        self.noidung.rowconfigure(0, weight=1)

        self.phan_trai = tk.Frame(self.noidung, bg="#ebebeb")
        self.phan_trai.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        self.phan_phai = tk.Frame(self.noidung, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        self.phan_phai.grid(row=0, column=1, sticky="nsew")

    def the_thong_ke(self, data_list):
        the_1 = tk.Frame(self.phan_trai, bg="#ebebeb")
        the_1.pack(fill="x", pady=(0, 20))
        the_1.columnconfigure((0, 1, 2), weight=1)

        cards = []
        for i, (title, value, color, icon) in enumerate(data_list):
            card = tk.Frame(the_1, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
            card.grid(row=0, column=i, sticky="nsew", padx=(0, 15))
            card.config(height=100)
            card.grid_propagate(False)

            tk.Frame(card, bg=color, height=4).pack(side="bottom", fill="x")
            content_f = tk.Frame(card, bg="white")
            content_f.pack(fill="both", expand=True, padx=15, pady=15)

            tk.Label(content_f, text=icon, font=("Arial", 15), bg="white", fg=color).pack(side="left", padx=(0, 10))
            text_f = tk.Frame(content_f, bg="white")
            text_f.pack(side="left", fill="y")

            tk.Label(text_f, text=title, bg="white", fg="#718096", font=("Arial", 9, "bold")).pack(anchor="w")
            tk.Label(text_f, text=value, bg="white", fg="#2D3748", font=("Arial", 18, "bold")).pack(anchor="w")
            cards.append(card)
        return cards

    def the_bieu_do(self, titles):
        the_2 = tk.Frame(self.phan_trai, bg="#ebebeb")
        the_2.pack(fill="x", pady=(0, 20))
        the_2.columnconfigure((0, 1), weight=1)

        for i in range(2):
            card_1 = tk.Frame(the_2, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
            card_1.grid(row=0, column=i, sticky="nsew", padx=(0, 15))
            card_1.config(height=200)
            card_1.grid_propagate(False)

            tk.Label(card_1, text=titles[i], bg="white", fg="#2D3748", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
            tk.Label(card_1, text="📊 [Biểu đồ giả lập]", bg="white", fg="#CBD5E0", font=("Arial", 10)).pack(expand=True)

    def lich_va_thong_bao(self, ds_lich, ds_tin):
        the_3 = tk.Frame(self.phan_trai, bg="#ebebeb")
        the_3.pack(fill="both", expand=True)
        the_3.columnconfigure((0, 1), weight=1)

        lich_frame = tk.Frame(the_3, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        lich_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        tk.Label(lich_frame, text="Lịch biểu hôm nay", bg="white", fg="#2D3748", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)

        for ten, gio in ds_lich:
            row = tk.Frame(lich_frame, bg="white")
            row.pack(fill="x", padx=15, pady=5)
            tk.Label(row, text=f"• {ten}", bg="white", font=("Arial", 9)).pack(side="left")
            tk.Label(row, text=gio, bg="white", fg="#718096", font=("Arial", 8)).pack(side="right")

        tb_frame = tk.Frame(the_3, bg="white", highlightthickness=1, highlightbackground="#E2E8F0")
        tb_frame.grid(row=0, column=1, sticky="nsew")
        tk.Label(tb_frame, text="Thông báo gần đây", bg="white", fg="#2D3748", font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
        for tin in ds_tin:
            tk.Label(tb_frame, text=f" • {tin}", bg="white", fg="#4A5568", font=("Arial", 9), anchor="w").pack(fill="x", padx=15, pady=4)

    def vinh_danh(self, ds_vinh_danh):
        tk.Label(self.phan_phai, text="Học sinh xuất sắc nhất tháng", bg="white", fg="#2D3748",
                 font=("Arial", 12, "bold"), justify="left").pack(anchor="w", padx=20, pady=20)

        items = []
        for ten, lop, diem in ds_vinh_danh:
            item = tk.Frame(self.phan_phai, bg="white")
            item.pack(fill="x", padx=20, pady=10)

            tk.Label(item, text="👤", font=("Arial", 14), bg="#EDF2F7", width=3).pack(side="left")
            info = tk.Frame(item, bg="white")
            info.pack(side="left", padx=10)

            tk.Label(info, text=ten, bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
            tk.Label(info, text=lop, bg="white", fg="#718096", font=("Arial", 8)).pack(anchor="w")
            tk.Label(item, text=diem, bg="white", fg="#48BB78", font=("Arial", 10, "bold")).pack(side="right")
            items.append(item)
        return items