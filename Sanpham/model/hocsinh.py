import csv
import os


class HocSinhModel:
    def __init__(self, csv_path, fields):
        self.csv_path = csv_path
        self.fields = fields

    def list(self):
        """Đọc toàn bộ dữ liệu từ file CSV và trả về danh sách dạng dictionary"""
        data = []
        if not os.path.exists(self.csv_path):
            return {"data": data}

        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Làm sạch dữ liệu khoảng trắng thừa giống logic cũ của bạn
                clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                if clean_row:
                    data.append(clean_row)
        return {"data": data}

    def delete(self, key, value):
        """Xóa học sinh có mã trùng khớp và cập nhật lại file CSV gốc"""
        if not os.path.exists(self.csv_path):
            return

        # Đọc dữ liệu cũ dữ lại những dòng không bị xóa
        keep_rows = []
        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                if str(clean_row.get(key)).strip() != str(value).strip():
                    keep_rows.append(clean_row)

        # Cập nhật lại STT tự động sau khi xóa để file CSV luôn chuẩn
        for i, row in enumerate(keep_rows, start=1):
            row['stt'] = str(i)

        # Ghi đè lại vào file CSV
        with open(self.csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(keep_rows)

    def insert(self, row_data):
        """Thêm một học sinh mới vào cuối file CSV"""
        file_exists = os.path.exists(self.csv_path)

        with open(self.csv_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_data)