import gspread
import pandas as pd


class GoogleSheetIntegrator:
    def __init__(self, json_path, sheet_name):
        self.gc = gspread.service_account(filename=json_path)
        self.sh = self.gc.open(sheet_name)
        self.worksheet = self.sh.sheet1

    def send_data(self, df):
        self.worksheet.clear()
        data_to_send = [df.columns.tolist()] + df.values.tolist()

        self.worksheet.append_rows(data_to_send)
        print(f"loaded {len(df)}")
