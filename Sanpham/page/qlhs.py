import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


class QLHSView:
    def __init__(self, parent):
        self.parent = parent
        self.color_navy = "#1e376d"
        current_dir = os.path.dirname(__file__)
        self.csv_path = os.path.join(os.path.dirname(current_dir), "database", "hocsinh.csv")

        self.draw()
        self.load_data()

    def draw(self):
        self.main_frame = tk.Frame(self.parent, bg="#f5f6fa")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # TIÊU ĐỀ
        tk.Label(self.main_frame, text="📚 QUẢN LÝ HỌC SINH",
                 font=("Arial", 16, "bold"), fg=self.color_navy, bg="#f5f6fa").pack(anchor="w", pady=(0, 15))

        #  THANH CÔNG CỤ
        toolbar = tk.Frame(self.main_frame, bg="#f5f6fa")
        toolbar.pack(fill="x", pady=(0, 15))

        tk.Label(toolbar, text=" Tìm kiếm:", font=("Arial", 10, "bold"), bg="#f5f6fa").pack(side="left")
        self.search_entry = tk.Entry(toolbar, font=("Arial", 10), width=35)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.insert(0, "Nhập tên, lớp hoặc mã HS...")

        # nhấn Enter
        self.search_entry.bind("<FocusIn>", lambda e: self.search_entry.delete(0,
                                                                               'end') if self.search_entry.get() == "Nhập tên, lớp hoặc mã HS..." else None)
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_data())
        self.search_entry.bind("<Return>", lambda e: self.search_data())

        #Thêm/Xóa
        btn_del = tk.Button(toolbar, text="Xóa học sinh", bg="#e74a3b", fg="white",
                            font=("Arial", 9, "bold"), command=self.delete_student, padx=15, bd=0, cursor="hand2")
        btn_del.pack(side="right", padx=5)

        btn_add = tk.Button(toolbar, text=" Thêm mới", bg="#1cc88a", fg="white",
                            font=("Arial", 9, "bold"), command=self.add_student_popup, padx=15, bd=0, cursor="hand2")
        btn_add.pack(side="right", padx=5)

        # BẢNG DỮ LIỆU
        table_frame = tk.Frame(self.main_frame, bg="white")
        table_frame.pack(fill="both", expand=True)

        columns = ("stt", "ho_ten", "ma_hs", "lop")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.tree.heading("stt", text="STT")
        self.tree.heading("ho_ten", text="Họ và Tên")
        self.tree.heading("ma_hs", text="Mã Học Sinh")
        self.tree.heading("lop", text="Lớp")

        self.tree.column("stt", width=60, anchor="center")
        self.tree.column("ho_ten", width=350, anchor="w")
        self.tree.column("ma_hs", width=150, anchor="center")
        self.tree.column("lop", width=100, anchor="center")

        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Phím Delete
        self.tree.bind("<Delete>", lambda e: self.delete_student())

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not os.path.exists(self.csv_path): return

        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                stt_raw = str(clean_row.get('stt', ''))
                stt_final = stt_raw.split('.')[0] if '.' in stt_raw else stt_raw

                self.tree.insert("", "end", values=(stt_final, clean_row.get('ho_ten', ''), clean_row.get('ma_hs', ''),
                                                    clean_row.get('lop', '')))

    def search_data(self):
        query = self.search_entry.get().lower()
        if query == "nhập tên, lớp hoặc mã hs...": return
        self.load_data()
        if query:
            for item in self.tree.get_children():
                v = self.tree.item(item)['values']
                # Tìm ở cả 3 cột: Tên(1), Mã(2), Lớp(3)
                if query not in str(v[1]).lower() and query not in str(v[2]).lower() and query not in str(v[3]).lower():
                    self.tree.delete(item)

    def add_student_popup(self):
        pop = tk.Toplevel(self.parent)
        pop.title("Thêm học sinh mới")
        pop.geometry("350x300")
        pop.grab_set()

        fields = [("Họ và Tên:", "name"), ("Mã Học Sinh:", "id"), ("Lớp:", "class")]
        entries = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(pop, text=label, font=("Arial", 10)).pack(pady=(10, 0))
            entries[key] = tk.Entry(pop, font=("Arial", 10), width=30)
            entries[key].pack(pady=5)

        entries["name"].focus_set()

        def save():
            name = entries["name"].get()
            mshs = entries["id"].get()
            lop = entries["class"].get()

            if not name or not mshs or not lop:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các thông tin")
                return

            # STT tự động
            current_count = len(self.tree.get_children(""))
            new_stt = str(current_count + 1)

            # Thêm
            self.tree.insert("", "end", values=(new_stt, name, mshs, lop))
            messagebox.showinfo("Thành công", f"Đã thêm học sinh {name}")
            pop.destroy()

        # Enter
        pop.bind("<Return>", lambda e: save())
        tk.Button(pop, text="Lưu thông tin ", bg=self.color_navy, fg="white",
                  font=("Arial", 10, "bold"), command=save, pady=8, padx=20).pack(pady=20)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn học sinh", "Bạn chưa chọn dòng nào để xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa học sinh đã chọn?"):
            for item in selected:
                self.tree.delete(item)