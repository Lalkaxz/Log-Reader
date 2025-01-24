import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog
import pandas as pd


class DatabaseHandler:
    last_opened_dir = ""

    @staticmethod
    def get_open_file(parent) -> str:
        start_dir = DatabaseHandler.last_opened_dir or "."

        fpath, _ = QFileDialog.getOpenFileName(parent, "Open file", start_dir, "Database files (*.db *.sqlite *.sqlite3 *.db3)")
        if fpath:
            DatabaseHandler.last_opened_dir = fpath.rsplit("/", 1)[0]

        return fpath


    @staticmethod
    def connect_database(path: str) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(path)
        except Exception as e:
            sys.exit(f"Failed to connect database: {e}")
            
        return conn
        

    @staticmethod
    def get_database_tables(db: sqlite3.Connection) -> list[str]:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except sqlite3.Error as e:
            print(f"Error getting tables list: {e}")
            return []
       
    
    @staticmethod
    def get_database_data(db: sqlite3.Connection, table: str) -> pd.DataFrame:
        data = pd.DataFrame()
        cursor = db.cursor()

        try:
            cursor.execute(f'PRAGMA table_info("{table}");')
            columns_info = cursor.fetchall()

            columns_names = [column[1] for column in columns_info]

        except sqlite3.Error as e:
            print(f"Error getting table data (columns): {e}")
            return data
        
        try: 
            cursor.execute(f'SELECT * FROM "{table}";')
            rows = cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Error getting table data: {e}")
            return data
            
        data = pd.DataFrame(data=rows, columns=columns_names)

        return data

