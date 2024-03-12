import tkinter as tk

class UI:
    def __init__(self):
        self._title = "Deferred Exam Scheduler"
        self._width = 500
        self._height= 300
        self._bg ='#ADD8E6'


    def get_title(self): return self._title
    def get_width(self): return self._width
    def get_height(self): return self._height
    def get_background(self): return self._bg
    
    def setup(self):
        self.root.geometry("500x300")
        self.root.configure(bg='#ADD8E6')

        frame = tk.Frame(self.root, bg='#ADD8E6')
        frame.pack(pady=20)

        upload_button = tk.Button(frame, text="Upload and Save Excel File", command=self.app.upload_file)
        #upload_button = tk.Button(frame, text="Upload and Save Excel File")
        #upload_button.pack()