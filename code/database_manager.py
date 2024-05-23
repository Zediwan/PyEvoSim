from __future__ import annotations
import datetime
import os
import csv

class DatabaseManager():
    folder_pathname: str = "data/"
    filename_start: str = "database_"
    filename_end: str = ".csv"
    
    def __init__(self, headers: list[str], name = "") -> None:
        self.creation_date: datetime.date = datetime.datetime.now()
        self.name: str = name + self.creation_date.strftime("%Y%m%d%H%M%S")
        self.csv_pathname: str = DatabaseManager.folder_pathname + DatabaseManager.filename_start + self.name + DatabaseManager.filename_end

        self.metadata: dict[str] = {}
        self.headers = headers

        try:
            with open(self.csv_pathname, mode="a", newline="") as file:
                writer: csv.DictWriter = csv.writer(file)
                writer.writerow(self.headers)
        except IOError as e:
            print(f"Error writing to CSV: {e}")
    
    def add_data(self, data_dict: dict[str,]):
        data = [data_dict.get(header, None) for header in self.headers]
        try:
            with open(self.csv_pathname, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except IOError as e:
            print(f"Error writing to CSV: {e}")

    @classmethod
    def get_newest_database(cls) -> DatabaseManager:
        pass
    