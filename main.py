import tkinter as tk
from tkinter import filedialog
import shutil
import os

def upload_and_save():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        new_file_path = os.path.join(downloads_path, "data.xlsx")
        shutil.copy(file_path, new_file_path)
        tk.messagebox.showinfo("Success", "File has been saved as 'data.xlsx' in Downloads.")

root = tk.Tk()
root.title("Deferred Exam Scheduler - v0.1")

# Set the window size
root.geometry("500x300")

# Set the background color
root.configure(bg='#ADD8E6')

frame = tk.Frame(root, bg='#ADD8E6')  # Apply the same background color to the frame
frame.pack(pady=20)

upload_button = tk.Button(frame, text="Upload and Save Excel File", command=upload_and_save)
upload_button.pack()

root.mainloop()