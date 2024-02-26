import tkinter as tk
from tkinter import messagebox

class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.selected_schedule = tk.StringVar()
        self.setup()

    def setup(self):
        self.root.title("Deferred Exam Scheduler")
        self.root.geometry("500x400")  # Increased height to accommodate new elements
        self.root.configure(bg='#D3D3D3')

        frame = tk.Frame(self.root, bg='#D3D3D3')
        frame.pack(pady=20)

        upload_button = tk.Button(frame, text="Upload Excel File", command=self.app.upload_file)
        upload_button.pack()

        # Schedules Listbox
        self.schedules_listbox = tk.Listbox(frame, height=3)
        schedules = ["Schedule 1 - Description", "Schedule 2 - Description", "Schedule 3 - Description"]
        for schedule in schedules:
            self.schedules_listbox.insert(tk.END, schedule)
        self.schedules_listbox.pack(pady=10)

        # Download Button
        download_button = tk.Button(frame, text="Download Selected Schedule", command=self.download_schedule)
        download_button.pack()

    def download_schedule(self):
        try:
            selection_index = self.schedules_listbox.curselection()[0]
            selected_schedule = self.schedules_listbox.get(selection_index)
            self.app.download_file(selected_schedule.split(' - ')[0])  # Assuming you only want the name part for downloading
            messagebox.showinfo("Success", f"{selected_schedule.split(' - ')[0]} downloaded successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a schedule to download")