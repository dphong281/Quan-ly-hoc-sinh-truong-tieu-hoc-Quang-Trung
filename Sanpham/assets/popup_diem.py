import tkinter as tk
from tkinter import messagebox
import threading


class DiemPopup:
    def __init__(self, parent, controller, student_info):
        self.parent = parent
        self.controller = controller
        self.student_info = student_info

        self.pop = tk.Toplevel(self.parent)
        self.pop.title("Nhập điểm học sinh")
        self.pop.geometry("380x350")
        self.pop.grab_set()

        # UI
        tk.Label(self.pop, text=f"Học sinh: {self.student_info['ho_ten']}", font=("Arial", 11, "bold")).pack(
            pady=(15, 5))
        tk.Label(self.pop, text=f"Mã HS: {self.student_info['ma_hs']}  |  Lớp: {self.student_info['lop']}",
                 font=("Arial", 10)).pack(pady=(0, 15))

        tk.Label(self.pop, text="Điểm giữa kỳ (0 - 10):").pack()
        self.ent_giua = tk.Entry(self.pop, font=("Arial", 11), width=15)
        self.ent_giua.pack(pady=5)
        self.ent_giua.insert(0, self.student_info['giua_cu'])

        tk.Label(self.pop, text="Điểm cuối kỳ (0 - 10):").pack()
        self.ent_cuoi = tk.Entry(self.pop, font=("Arial", 11), width=15)
        self.ent_cuoi.pack(pady=5)
        self.ent_cuoi.insert(0, self.student_info['cuoi_cu'])

        self.lbl_tb = tk.Label(self.pop, text="TB cả năm: --", font=("Arial", 10, "bold"), fg="#1e376d")
        self.lbl_tb.pack(pady=10)

        # Bind sự kiện
        self.ent_giua.bind("<KeyRelease>", self.cap_nhat_tb)
        self.ent_cuoi.bind("<KeyRelease>", self.cap_nhat_tb)

        tk.Button(self.pop, text="Lưu điểm", bg="#1e376d", fg="white", command=self.luu_diem).pack(pady=10)

    def cap_nhat_tb(self, e=None):
        g = self.controller.kiem_tra_diem(self.ent_giua.get())
        c = self.controller.kiem_tra_diem(self.ent_cuoi.get())
        if g is not None and c is not None:
            tb = round((g + c * 2) / 3, 1)
            self.lbl_tb.config(text=f"TB cả năm: {tb}")
        else:
            self.lbl_tb.config(text="TB cả năm: --")

    def luu_diem(self):
        val_giua = self.ent_giua.get().strip()
        val_cuoi = self.ent_cuoi.get().strip()

        # Kiểm tra không để trống
        if not val_giua or not val_cuoi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ điểm!")
            return

        # Kiểm tra định dạng số
        def is_valid_score(score_str):
            try:
                score = float(score_str.replace(",", "."))
                return 0 <= score <= 10
            except ValueError:
                return False

        if not is_valid_score(val_giua) or not is_valid_score(val_cuoi):
            messagebox.showerror("Lỗi", "Điểm phải là số thực từ 0 đến 10!")
            return

        g = float(val_giua.replace(",", "."))
        c = float(val_cuoi.replace(",", "."))

        self.pop.destroy()

        def _task_luu():
            tb = round((g + c * 2) / 3, 1)
            self.controller.query.update_row(self.controller.diem_path, "ma_hs", self.student_info['ma_hs'],
                                             {"giua_ky": g, "cuoi_ky": c, "tb_ca_nam": tb})
            self.parent.after(0, self.controller.tai_du_lieu_async)

        threading.Thread(target=_task_luu, daemon=True).start()

