from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ...utils.fileHandler import FileHandler
from ...utils.databaseHandler import DatabaseHandler

# QAction for handle open text files.
class OpenFileAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Open file", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+O")
        self.triggered.connect(self.handle_open_file) # Connect handler function.

    # Handler open text file.
    def handle_open_file(self, file_path: str = None) -> None:
        # If file path not provided, open file dialog.
        if not file_path:
            file_path = FileHandler.get_open_file(self.parent)

        if file_path:
            file_content = FileHandler.read_file(self.parent, file_path) # Read file content from path.
            if not file_content:
                return
            self.parent.file_viewer.display_file_content(file_content, file_path) # Display file content on file viewer widget.
            self.parent.file_list.add_file_to_list(file_path) # Add file to display list.
        else:
            return
        
        # Set current widget to file environment.
        self.parent.init_file_env() 
    

# QAction for handle open database files.
class OpenDatabaseAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Open database file", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+D")
        self.triggered.connect(self.handle_open_database) # Connect handler function.

    # Handler open database file.
    def handle_open_database(self, file_path: str = None) -> None:
        # If database file path is not provided, open file dialog.
        if not file_path:
            file_path = DatabaseHandler.get_open_file(self.parent)

        if file_path:
            conn = DatabaseHandler.connect_database(self.parent, file_path) # Connect to database.
            if conn == None: 
                return
            tables = DatabaseHandler.get_database_tables(self.parent, conn) # Get list tables.
            if tables == None: 
                return
            self.parent.file_list.add_tables_to_list(tables, file_path) # Add tables to display list.
            conn.close()
        else:
            return
        
        # Set current widget to file environment.
        self.parent.init_file_env()


# QAction for handle exit app.
class ExitAppAction(QAction):
    def __init__(self, parent=None) -> None:
        super().__init__(text="Exit", parent=parent)
        self.parent = parent
        self.setShortcut("Ctrl+Q")
        self.triggered.connect(QApplication.exit) # Exit application.



        
