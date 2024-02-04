import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

def copy_file_to_downloads(file_path, new_file_name="data.xlsx"):
    if file_path:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        new_file_path = os.path.join(downloads_path, new_file_name)
        shutil.copy(file_path, new_file_path)
        return new_file_path
    return None

def upload_and_save():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    result = copy_file_to_downloads(file_path)
    if result:
        messagebox.showinfo("Success", f"File has been saved as '{os.path.basename(result)}' in Downloads.")

root = tk.Tk()
root.title("Deferred Exam Scheduler")
# Set the window size
root.geometry("500x300")

# Set the background color
root.configure(bg='#ADD8E6')
frame = tk.Frame(root)
frame.pack(pady=20)

upload_button = tk.Button(frame, text="Upload and Save Excel File", command=upload_and_save)
upload_button.pack()

root.mainloop()