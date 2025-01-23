from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler


class OpenFileAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Open file", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+O")
        self.triggered.connect(self.handle_open_file)


    def handle_open_file(self, file_path: str = None) -> None:

        if not file_path:
            file_path = FileHandler.get_open_file(self.parent)

        if file_path:
            file_content = FileHandler.read_file(file_path)
            self.parent.file_viewer.display_file_content(file_content, file_path)
            self.parent.file_list.add_file_to_list(file_path)
        else:
            return
    


class OpenDatabaseAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Open database file", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+D")
        self.triggered.connect(self.handle_open_database)


    def handle_open_database(self, file_path: str = None) -> None:

        if not file_path:
            file_path = DatabaseHandler.get_open_file(self.parent)

        if file_path:
            conn = DatabaseHandler.connect_database(file_path)
            tables = DatabaseHandler.get_database_tables(conn)
            self.parent.file_list.add_tables_to_list(tables, file_path)
            conn.close()
        else:
            return



class ExitAppAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Exit", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+Q")
        self.triggered.connect(QApplication.exit)



        
