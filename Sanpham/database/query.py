import pandas as pd
import os


class HocSinhQuery:
    def __init__(self, file_path="database/hocsinh.csv"):
        self.file_path = file_path
        self.columns = ["stt", "ho_ten", "ma_hs", "lop"]

        # nếu chưa có file → tạo file mới
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.file_path, index=False)

    # ================= LOAD =================
    def _load(self):
        return pd.read_csv(self.file_path)

    def _save(self, df):
        df.to_csv(self.file_path, index=False)

    # ================= LIST =================
    def list(self, page=1, page_size=10):
        df = self._load()

        total = len(df)
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "page": page,
            "page_size": page_size,
            "total_records": total,
            "total_pages": (total + page_size - 1) // page_size,
            "data": df.iloc[start:end]
        }

    # ================= SEARCH =================
    def search(self, keyword):
        df = self._load()

        result = df[
            df["ho_ten"].astype(str).str.contains(keyword, case=False, na=False) |
            df["ma_hs"].astype(str).str.contains(keyword, case=False, na=False) |
            df["lop"].astype(str).str.contains(keyword, case=False, na=False)
        ]

        return result

    # ================= CREATE =================
    def create(self, ho_ten, ma_hs, lop):
        df = self._load()

        # check trùng mã HS
        if ma_hs in df["ma_hs"].values:
            raise ValueError(f"Mã HS '{ma_hs}' đã tồn tại")

        # tạo STT
        if df.empty:
            stt = 1
        else:
            stt = int(df["stt"].max()) + 1

        new_row = pd.DataFrame([{
            "stt": stt,
            "ho_ten": ho_ten,
            "ma_hs": ma_hs,
            "lop": lop
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        self._save(df)

        return True

    # ================= UPDATE =================
    def update(self, stt, ho_ten, ma_hs, lop):
        df = self._load()

        # check trùng mã HS (trừ chính nó)
        check = df[(df["ma_hs"] == ma_hs) & (df["stt"] != stt)]
        if not check.empty:
            raise ValueError(f"Mã HS '{ma_hs}' đã tồn tại")

        df.loc[df["stt"] == stt, ["ho_ten", "ma_hs", "lop"]] = [ho_ten, ma_hs, lop]

        self._save(df)
        return True

    # ================= DELETE =================
    def delete(self, stt):
        df = self._load()

        df = df[df["stt"] != stt]

        # reset lại STT cho đẹp
        df = df.reset_index(drop=True)
        df["stt"] = df.index + 1

        self._save(df)
        return True

    # ================= GET ONE =================
    def get_by_stt(self, stt):
        df = self._load()

        result = df[df["stt"] == stt]
        if result.empty:
            return None

        return result.iloc[0].to_dict()

    # ================= MAX =================
    def max(self):
        df = self._load()

        if df.empty:
            return 0
        return int(df["stt"].max())