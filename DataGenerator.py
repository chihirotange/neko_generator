import pandas as pd
import constants

class DataGenerator:
    def __init__(self, sheet_id = constants.SHEET_ID):
        self.sheet_id = sheet_id
        self.data = self.gsheet_to_pandas()

    def gsheet_to_pandas(self):
        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/export?format=csv") #trick convert sheet thanh CSV bang cach thay doi URL
        return df