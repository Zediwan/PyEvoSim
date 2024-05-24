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
        
        if os.path.isfile(self.csv_pathname):
            raise ValueError("There is already a database with the same name.")

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
    def get_newest_database_pathname(cls) -> str:
        newest_file = None
        newest_date = datetime.datetime.min

        for file in os.listdir(cls.folder_pathname):
            if file.startswith(cls.filename_start) and file.endswith(cls.filename_end):
                creation_date_str = file[len(cls.filename_start):-len(cls.filename_end)]
                creation_date = datetime.datetime.strptime(creation_date_str, "%Y%m%d%H%M%S")
                if creation_date > newest_date:
                    newest_date = creation_date
                    newest_file = file
        if newest_file:
            return DatabaseManager.folder_pathname + newest_file
        else:
            return None
    