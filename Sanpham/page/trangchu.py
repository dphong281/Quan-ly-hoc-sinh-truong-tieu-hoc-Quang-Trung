import tkinter as tk
from tkinter import ttk


class TrangChuView:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"
        self.draw()

    def draw(self):
        # --- TẠO CANVAS VÀ SCROLLBAR ---
        self.canvas = tk.Canvas(self.parent, bg="#f5f6fa", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f6fa")

        # Cấu hình vùng cuộn mỗi khi nội dung thay đổi
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack Canvas và Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- LĂN CHUỘT ---
        self.parent.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- NỘI DUNG XẾP CHỒNG ---
        container = tk.Frame(self.scrollable_frame, bg="#f5f6fa", padx=30, pady=20)
        container.pack(fill="both", expand=True)

        # 1. PHẦN TIN TỨC
        self.create_section(container, "📰 TIN TỨC MỚI", "#4e73df", [
            "• Thông báo lịch thi cuối kỳ II cho toàn thể học sinh khối 1 đến khối 5.",
            "• Chúc mừng các em học sinh đạt giải cao trong kỳ thi Trạng Nguyên Tiếng Việt cấp Thành phố.",
            "• Nhà trường triển khai mô hình 'Cổng trường an toàn giao thông' phối hợp với công an phường.",
            "• Hướng dẫn phụ huynh làm thủ tục nộp hồ sơ tuyển sinh trực tuyến cho học sinh lớp 1.",
            "• Thông báo thay đổi thực đơn bán trú áp dụng từ tuần sau."
        ])

        # 2. PHẦN SỰ KIỆN NỔI BẬT
        self.create_section_event(container, "🌟 SỰ KIỆN NỔI BẬT", "#e74a3b")

        # 3. PHẦN HOẠT ĐỘNG ĐOÀN ĐỘI
        self.create_section(container, "🚩 HOẠT ĐỘNG ĐOÀN ĐỘI", "#1cc88a", [
            "📅 22/04: Ngày hội đọc sách và quyên góp sách cho thư viện vùng cao.",
            "📅 26/04: Tổ chức Đại hội Cháu ngoan Bác Hồ và tuyên dương các đội viên ưu tú.",
            "📅 28/04: Phong trào thu gom kế hoạch nhỏ đợt 3 tại sảnh sau nhà trường.",
            "📅 30/04: Chương trình văn nghệ chào mừng ngày giải phóng miền Nam 30/4.",
            "📅 15/05: Lễ kỷ niệm ngày thành lập Đội Thiếu niên Tiền phong Hồ Chí Minh."
        ])

        # Thêm khoảng trống dưới cùng
        tk.Frame(container, height=50, bg="#f5f6fa").pack()

    # --- CÁC HÀM XỬ LÝ CUỘN ---
    def _on_mousewheel(self, event):
        """Xử lý lăn chuột (Windows)"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_canvas_configure(self, event):
        """Đảm bảo chiều rộng của nội dung bằng chiều rộng canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    # --- HÀM TẠO GIAO DIỆN ---
    def create_section(self, parent, title, color, items):
        frame = tk.Frame(parent, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdcdc")
        frame.pack(fill="x", pady=10)

        lbl_title = tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg=color, fg="white", pady=10, anchor="w",
                             padx=15)
        lbl_title.pack(fill="x")

        for text in items:
            lbl = tk.Label(frame, text=text, font=("Arial", 10), bg="white", fg="#333",
                           anchor="w", justify="left", wraplength=800, pady=10, padx=20)
            lbl.pack(fill="x")
            tk.Frame(frame, height=1, bg="#f0f0f0").pack(fill="x", padx=20)

    def create_section_event(self, parent, title, color):
        frame = tk.Frame(parent, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdcdc")
        frame.pack(fill="x", pady=10)

        lbl_title = tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg=color, fg="white", pady=10, anchor="w",
                             padx=15)
        lbl_title.pack(fill="x")

        img_sim = tk.Frame(frame, bg="#eaecf4", height=200)
        img_sim.pack(fill="x", padx=20, pady=15)
        tk.Label(img_sim, text="[ HÌNH ẢNH SỰ KIỆN LỚN ]", bg="#eaecf4", font=("Arial", 14), fg="#aeb1be").place(
            relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Đại lễ kỷ niệm 50 năm ngày thành lập trường", font=("Arial", 13, "bold"), bg="white",
                 fg=self.color_navy).pack(padx=20, anchor="w")

        desc = ("Đây là sự kiện lớn nhất trong năm học 2025-2026 nhằm tri ân các thế hệ giáo viên và học sinh. "
                "Chương trình bao gồm các tiết mục nghệ thuật đặc sắc...")

        tk.Label(frame, text=desc, font=("Arial", 10), bg="white", fg="#555", justify="left", wraplength=800, padx=20,
                 pady=10).pack(fill="x")