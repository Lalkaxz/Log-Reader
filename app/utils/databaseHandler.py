import sqlite3
import sys
from PyQt6.QtWidgets import QFileDialog
import pandas as pd
from .errorHandler import ErrorHandler


class DatabaseHandler:
    last_opened_dir = ""

    # Open file dialog and return file path.
    @staticmethod
    def get_open_file(parent) -> str:
        start_dir = DatabaseHandler.last_opened_dir or "." # If last opened direction is provided, use it for file dialog.

        fpath, _ = QFileDialog.getOpenFileName(parent, "Open file", start_dir, "Database files (*.db *.sqlite *.sqlite3 *.db3)")
        if fpath:
            DatabaseHandler.last_opened_dir = fpath.rsplit("/", 1)[0] # Set last opened direction.

        return fpath

    # Return database connection from path.
    @staticmethod
    def connect_database(parent, path: str) -> sqlite3.Connection | None:
        try:
            conn = sqlite3.connect(path)
        except sqlite3.Error as e:
            ErrorHandler.show_error_message(f"Failed to connect database: {e}", parent=parent)
            return None
        
        return conn
        
    # Return list of table names from database connection.
    @staticmethod
    def get_database_tables(parent, db: sqlite3.Connection) -> list[str]:
        try:
            # Initialize cursor and fetch all table names.
            cursor = db.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tables
        except sqlite3.Error as e:
            ErrorHandler.show_error_message(f"Error getting tables list: {e}", parent=parent)
            return []
       
    # Return database table data.
    @staticmethod
    def get_database_data(parent, db: sqlite3.Connection, table: str) -> pd.DataFrame | None:
        # Initialize cursor.
        cursor = db.cursor()

        # Fetch column names from database table.
        try:
            cursor.execute(f'PRAGMA table_info("{table}");')
            columns_info = cursor.fetchall()
            # Get list of table column names.
            column_names = [column[1] for column in columns_info]

        except sqlite3.Error as e:
            ErrorHandler.show_error_message(f"Error getting table data (columns): {e}", parent=parent)
            cursor.close()
            return None
        
        # Fetch rows data from database table.
        try: 
            cursor.execute(f'SELECT * FROM "{table}";')
            rows = cursor.fetchall()

        except sqlite3.Error as e:
            ErrorHandler.show_error_message(f"Error getting table data: {e}", parent=parent)
            cursor.close()
            return None
        # Initialize data class.
        data = pd.DataFrame(data=rows, columns=column_names)

        cursor.close()
        return data

