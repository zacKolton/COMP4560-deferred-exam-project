import tkinter as tk
from tkinter import filedialog, messagebox 
from scheduler.scheduler import Scheduler
from user_interface.UI import UI



class App:
    def __init__(self, root):
        self.root = root
        self.scheduler = Scheduler()
        self.ui = UI(root, self.scheduler)  # Pass the scheduler instance to UI

    def run(self):
        self.root.title(self.ui.get_title())
        self.root.geometry(f"{self.ui.get_width()}x{self.ui.get_height()}")

        self.print_settings()
        self.root.mainloop()

    def print_settings(self):
        print("App Title: " + self.ui.get_title())
        print("App Window Width: " + str(self.ui.get_width()))
        print("App Window Height: " + str(self.ui.get_height()))

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path != "":
            try:
                schedule = self.scheduler.create_schedule(file_path)
                messagebox.showinfo("Success", "The schedule has been successfully created.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")