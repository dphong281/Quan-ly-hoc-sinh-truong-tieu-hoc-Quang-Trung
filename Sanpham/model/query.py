import pandas as pd
import os

class Query:
    def __init__(self, db_folder="database"):
        # Tự động lấy đường dẫn thư mục database
        self.db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_folder)

    def _get_path(self, filename):
        return os.path.join(self.db_dir, filename)

    # Đọc file bất kỳ
    def read_csv(self, filename):
        path = self._get_path(filename)
        if not os.path.exists(path):
            return pd.DataFrame()
        return pd.read_csv(path)

    # Ghi file bất kỳ
    def save_csv(self, df, filename):
        path = self._get_path(filename)
        df.to_csv(path, index=False, encoding="utf-8")

    # --- HÀM NGHIỆP VỤ (Đã xử lý bằng Pandas) ---

    def get_all(self, filename):
        """Lấy toàn bộ dữ liệu dưới dạng danh sách từ điển"""
        df = self.read_csv(filename)
        return df.to_dict(orient='records')

    def update_row(self, filename, key_col, key_val, update_dict):
        """Cập nhật một dòng dựa trên key"""
        df = self.read_csv(filename)
        # Tìm dòng có key khớp và cập nhật giá trị
        for col, val in update_dict.items():
            df.loc[df[key_col].astype(str).str.strip() == str(key_val).strip(), col] = val
        self.save_csv(df, filename)

    def delete_row(self, filename, key_col, key_val):
        """Xóa một dòng dựa trên key"""
        df = self.read_csv(filename)
        df = df[df[key_col].astype(str).str.strip() != str(key_val).strip()]
        self.save_csv(df, filename)