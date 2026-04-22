import tkinter as tk
from tkinter import messagebox
import csv
import os


class DanhGiaView:
    def __init__(self, master):
        self.master = master
        self.color_navy = "#1e376d"

        # Thử tìm file theo nhiều cấp để chắc chắn
        current_dir = os.path.dirname(__file__)  # Thư mục 'page'
        # Lùi lại 1 cấp để vào 'Sanpham' rồi vào 'database'
        self.csv_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")

        # Nếu vẫn không thấy, thử tìm ngay tại thư mục gốc của project
        if not os.path.exists(self.csv_path):
            # Lùi thêm 1 cấp nữa ra khỏi 'Sanpham'
            project_root = os.path.dirname(os.path.dirname(current_dir))
            self.csv_path = os.path.join(project_root, "database", "hocsinh.csv")

        self.build_ui()

    def build_ui(self):
        # Tiêu đề
        tk.Label(
            self.master, text="📋 ĐÁNH GIÁ THEO MÃ HỌC SINH",
            font=("Arial", 20, "bold"), bg="#f5f6fa", fg=self.color_navy
        ).pack(pady=(30, 20))

        # Khung nhập liệu
        form_frame = tk.Frame(self.master, bg="white", bd=1, relief="solid", padx=30, pady=30)
        form_frame.pack(padx=50, fill="x")

        # 1. Nhập Mã học sinh
        tk.Label(form_frame, text="Nhập Mã HS:", bg="white", font=("Arial", 11, "bold")).grid(row=0, column=0,
                                                                                              sticky="w", pady=10)

        search_frame = tk.Frame(form_frame, bg="white")
        search_frame.grid(row=0, column=1, padx=20, sticky="w")

        self.ent_ma_hs = tk.Entry(search_frame, font=("Arial", 11), width=20, bd=1, relief="solid")
        self.ent_ma_hs.pack(side="left")

        btn_check = tk.Button(search_frame, text="Kiểm tra", command=self.search_student, bg=self.color_navy,
                              fg="white", font=("Arial", 9, "bold"))
        btn_check.pack(side="left", padx=10)

        # 2. Hiển thị thông tin tìm thấy (Read-only)
        tk.Label(form_frame, text="Họ tên:", bg="white", font=("Arial", 11, "bold")).grid(row=1, column=0, sticky="w",
                                                                                          pady=10)
        self.lbl_name = tk.Label(form_frame, text="...", bg="white", font=("Arial", 11, "italic"), fg="blue")
        self.lbl_name.grid(row=1, column=1, padx=20, sticky="w")

        tk.Label(form_frame, text="Lớp:", bg="white", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w",
                                                                                       pady=10)
        self.lbl_lop = tk.Label(form_frame, text="...", bg="white", font=("Arial", 11, "italic"), fg="blue")
        self.lbl_lop.grid(row=2, column=1, padx=20, sticky="w")

        # 3. Xếp loại
        tk.Label(form_frame, text="Xếp loại:", bg="white", font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w",
                                                                                            pady=10)
        self.rating_var = tk.StringVar(value="Tốt")
        radio_frame = tk.Frame(form_frame, bg="white")
        radio_frame.grid(row=3, column=1, sticky="w", padx=20)
        for text in ["Tốt", "Khá", "Cần cố gắng"]:
            tk.Radiobutton(radio_frame, text=text, variable=self.rating_var, value=text, bg="white").pack(side="left",
                                                                                                          padx=10)

        # 4. Nhận xét
        tk.Label(form_frame, text="Nhận xét:", bg="white", font=("Arial", 11, "bold")).grid(row=4, column=0,
                                                                                            sticky="nw", pady=10)
        self.txt_review = tk.Text(form_frame, height=4, width=45, font=("Arial", 11), bd=1, relief="solid")
        self.txt_review.grid(row=4, column=1, padx=20, pady=10)

        # 5. Nút lưu
        tk.Button(
            form_frame, text="LƯU ĐÁNH GIÁ", bg="#28a745", fg="white",
            font=("Arial", 11, "bold"), padx=30, pady=10, command=self.save_action
        ).grid(row=5, column=1, sticky="e", pady=10)

    def search_student(self):
        ma_nhap = self.ent_ma_hs.get().strip().upper()
        found = False

        if not os.path.exists(self.csv_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {self.csv_path}")
            return

        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Kiểm tra cột ma_hs trong file csv của bạn
                if row['ma_hs '].strip().upper() == ma_nhap:
                    self.lbl_name.config(text=row['ho_ten '])
                    self.lbl_lop.config(text=row['lop'])
                    found = True
                    break

        if not found:
            self.lbl_name.config(text="Không tìm thấy!")
            self.lbl_lop.config(text="...")
            messagebox.showwarning("Thông báo", "Mã học sinh không tồn tại!")

    def save_action(self):
        name = self.lbl_name.cget("text")
        if name == "..." or name == "Không tìm thấy!":
            messagebox.showwarning("Lỗi", "Vui lòng nhập đúng mã học sinh trước khi lưu!")
            return

        messagebox.showinfo("Thành công", f"Đã lưu đánh giá cho học sinh {name}")