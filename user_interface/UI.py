import tkinter as tk

class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup()

    
    def setup(self):
        self.root.title("Deferred Exam Scheduler")
        self.root.geometry("500x300")
        self.root.configure(bg='#ADD8E6')

        frame = tk.Frame(self.root, bg='#ADD8E6')
        frame.pack(pady=20)

        upload_button = tk.Button(frame, text="Upload and Save Excel File", command=self.app.upload_file)
        upload_button.pack()