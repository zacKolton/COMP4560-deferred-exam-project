from tkinter import filedialog, messagebox
# from scheduler.schedule_creator import ScheduleCreator


class App:
    def __init__(self, ui):
        self.ui = ui

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                #scheduler = ScheduleCreator()
                #schedule = scheduler.create_schedule(file_path)

                messagebox.showinfo("Success", "The schedule has been successfully created.")
            except Exception as e:
                 messagebox.showerror("Error", f"An error occurred: {e}")