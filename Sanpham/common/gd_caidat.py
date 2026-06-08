import customtkinter as ctk


class CaiDatView:
    def __init__(self, master, username):
        self.master = master
        self.username = username


        self.header()
        self.than_giao_dien()
        self.menu_trai()
        self.noi_dung_phai()

    def header(self):
        header_frame = ctk.CTkFrame(self.master, fg_color="#3cb3de", height=50, corner_radius=0)
        header_frame.pack(fill="x")

        ctk.CTkLabel(
            header_frame, text="CÀI ĐẶT", font=("Arial", 14, "bold"), text_color="white"
        ).pack(side="left", padx=20, pady=12)

    def than_giao_dien(self):
        self.body_frame = ctk.CTkFrame(self.master, fg_color="#f8fafc", corner_radius=0)
        self.body_frame.pack(fill="both", expand=True, padx=15, pady=15)

    def menu_trai(self):
        self.left_menu = ctk.CTkFrame(
            self.body_frame, fg_color="white", width=200, corner_radius=5, border_width=1, border_color="#e2e8f0"
        )
        self.left_menu.pack(side="left", fill="y", padx=(0, 15))
        self.left_menu.pack_propagate(False)

        self.menu_buttons = {}
        for text in ["Hệ thống", "Bảo mật", "Giới thiệu"]:
            btn = ctk.CTkButton(
                self.left_menu, text=text if text != "Hệ thống" else "Hệ thống chung",
                font=("Arial", 12, "bold"), fg_color="white", text_color="#4a5568",
                hover_color="#f0f0f0", anchor="w", corner_radius=0
            )
            btn.pack(fill="x", pady=5, padx=10)
            self.menu_buttons[text] = btn

    def noi_dung_phai(self):
        self.right_content = ctk.CTkFrame(
            self.body_frame, fg_color="white", corner_radius=5, border_width=1, border_color="#e2e8f0"
        )
        self.right_content.pack(side="left", fill="both", expand=True)

        self.khung_he_thong = ctk.CTkFrame(self.right_content, fg_color="white")
        self.khung_bao_mat = ctk.CTkFrame(self.right_content, fg_color="white")
        self.khung_about = ctk.CTkFrame(self.right_content, fg_color="white")

        # Đặt các khung chồng lên nhau
        for f in [self.khung_he_thong, self.khung_bao_mat, self.khung_about]:
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- Nội dung Khung Hệ thống ---
        ctk.CTkLabel(self.khung_he_thong, text="[ THÔNG TIN TÀI KHOẢN ]", text_color="#3cb3de",
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=20)
        self.ent_ho_ten = self._tao_input(self.khung_he_thong, "Họ và Tên:")
        self.ent_email = self._tao_input(self.khung_he_thong, "Email:")
        self.ent_sdt = self._tao_input(self.khung_he_thong, "Số điện thoại:")
        self.btn_save = ctk.CTkButton(self.khung_he_thong, text="Lưu", fg_color="#3cb3de", width=100)
        self.btn_save.pack(anchor="w", padx=20, pady=20)

        # --- Nội dung Khung Bảo mật ---
        ctk.CTkLabel(self.khung_bao_mat, text="[ BẢO MẬT ]", text_color="#3cb3de", font=("Arial", 12, "bold")).pack(
            anchor="w", padx=20, pady=20)
        self.ent_pass = self._tao_input(self.khung_bao_mat, "Mật khẩu:", show="*")
        self.ent_newpass = self._tao_input(self.khung_bao_mat, "Mật khẩu mới:", show="*")
        self.ent_renewpass = self._tao_input(self.khung_bao_mat, "Nhập lại mật khẩu:", show="*")
        self.btn_change = ctk.CTkButton(self.khung_bao_mat, text="Đổi mật khẩu", fg_color="#3cb3de", width=150)
        self.btn_change.pack(anchor="w", padx=20, pady=20)

        # --- Nội dung Khung Giới thiệu ---
        ctk.CTkLabel(self.khung_about, text="GIỚI THIỆU", font=("Arial", 14, "bold")).pack(pady=20)
        ctk.CTkLabel(self.khung_about, text="Phần mềm Quản lý Học sinh v1.0\nNhóm phát triển : Nhóm 6\n Liên hệ: danhphong28011@gmail.com").pack()

        self.khung_he_thong.tkraise()

    def _tao_input(self, parent, label, show=""):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(frame, text=label, width=150, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(frame, show=show)
        entry.pack(side="left", fill="x", expand=True)
        return entry