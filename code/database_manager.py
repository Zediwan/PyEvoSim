from __future__ import annotations
import datetime

class DatabaseManager():
    folder_pathname: str = "data/"
    filename_start: str = "database"
    filename_end: str = ".csv"
    
    def __init__(self, name = "") -> None:
        self.creation_date: datetime.date = datetime.datetime.now()
        self.name: str = name + self.creation_date.strftime("%Y%m%d%H%M%S")
        self.csv_pathname: str = DatabaseManager.folder_pathname + DatabaseManager.filename_start + self.name + DatabaseManager.filename_end
        self.metadata: dict[str, float] = {}

    @classmethod
    def get_newest_database(cls) -> DatabaseManager:
        pass