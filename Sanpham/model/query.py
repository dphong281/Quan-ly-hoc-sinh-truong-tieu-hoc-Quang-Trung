import pandas as pd
import os

class Query:
    def __init__(self, db_folder="database"):
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

    # HÀM LÀM VIỆC

    def get_all(self, filename):
        df = self.read_csv(filename)
        return df.to_dict(orient='records')

    def update_row(self, filename, key_col, key_val, update_dict):
        df = self.read_csv(filename)
        for col, val in update_dict.items():
            df.loc[df[key_col].astype(str).str.strip() == str(key_val).strip(), col] = val
        self.save_csv(df, filename)

    def delete_row(self, filename, key_col, key_val):
        df = self.read_csv(filename)
        df = df[df[key_col].astype(str).str.strip() != str(key_val).strip()]
        self.save_csv(df, filename)