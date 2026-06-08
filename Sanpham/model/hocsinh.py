import csv
import os
import pandas as pd


class HocSinhModel:
    def __init__(self, csv_path, fields):
        self.csv_path = csv_path
        self.fields = fields

    def list(self):
        data = []
        if not os.path.exists(self.csv_path):
            return {"data": data}

        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                if clean_row:
                    data.append(clean_row)
        return {"data": data}

    def delete(self, key, value):
        if not os.path.exists(self.csv_path):
            return

        keep_rows = []
        with open(self.csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
                if str(clean_row.get(key)).strip() != str(value).strip():
                    keep_rows.append(clean_row)

        for i, row in enumerate(keep_rows, start=1):
            row['stt'] = str(i)

        with open(self.csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(keep_rows)

    def insert(self, row_data):
        if not os.path.exists(self.csv_path):
            return

        with open(self.csv_path, mode='a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writerow(row_data)

    def update(self, key_field, key_value, updated_data):
        all_students = self.list()["data"]

        for row in all_students:
            if str(row.get(key_field, '')).strip() == str(key_value).strip():
                for k, v in updated_data.items():
                    row[k] = v
                break

        with open(self.csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(all_students)

    def export_to_excel(self, file_path):
        data = self.list()["data"]
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    def import_from_excel(self, file_path):
        """Nhập dữ liệu từ Excel và ghi đè hoặc bổ sung vào CSV"""
        try:
            # Đọc file Excel
            df = pd.read_excel(file_path)

            # Đảm bảo các cột trong Excel khớp với fields của bạn
            # Bạn có thể yêu cầu file Excel phải có đúng cột: stt, ho_ten, ma_hs, lop
            new_data = df.to_dict(orient='records')

            # Xử lý làm sạch dữ liệu trước khi lưu
            cleaned_data = []
            for row in new_data:
                # Ép kiểu và xóa khoảng trắng thừa
                clean_row = {k.strip(): str(v).strip() for k, v in row.items()}
                cleaned_data.append(clean_row)

            # Ghi đè vào file CSV hiện tại
            with open(self.csv_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fields)
                writer.writeheader()
                writer.writerows(cleaned_data)

            return True
        except Exception as e:
            print(f"Lỗi khi import Excel: {e}")
            return False