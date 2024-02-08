import os
import shutil
from tkinter import filedialog, messagebox


class App:
    def __init__(self, ui):
        self.ui = ui

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        result = self.process_file(file_path)
        if result:
            messagebox.showinfo("Success", f"File has been saved as '{os.path.basename(result)}' in Downloads.")

    def process_file(self, file_path, new_file_name="data.xlsx"):
        if file_path:
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads') 
            new_file_path = os.path.join(downloads_path, new_file_name)
            #shutil.copy(file_path, new_file_path)
            return new_file_path
        return None