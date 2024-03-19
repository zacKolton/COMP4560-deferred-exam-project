import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk

class UI:
    def __init__(self, master, scheduler):
        self.root = master
        self.scheduler = scheduler
        self._title = "Deferred Exam Scheduler"
        self._width = 700
        self._height = 400

        self.root.title(self._title)
        self.root.geometry(f"{self._width}x{self._height}")

        try:
            pil_image = Image.open("./branding/background.jpg")
            resized_image = pil_image.resize((self._width, self._height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.background_label = tk.Label(self.root, image=self.photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading the background image: {e}")
            self.root.configure(bg='gray')

        self.upload_button = tk.Button(self.root, text="Upload and Generate Schedule", command=self.upload_file)
        self.upload_button.configure(
            font=('Helvetica', 12, 'bold'), 
            fg='black', 
            bg='#0078D7', 
            activebackground='#0053ba', 
            activeforeground='black', 
            bd=2, 
            relief='raised', 
            padx=10, 
            pady=5
        )
        self.upload_button.place(x=self._width // 2, y=self._height // 2, anchor='center')

        self.settings_button = tk.Button(self.root, text='⚙', command=self.open_settings)
        self.settings_button.configure(
            font=('Helvetica', 14, 'bold'), 
            fg='black', 
            bg='gray', 
            bd=0, 
            relief='flat', 
            highlightthickness=0
        )
        self.settings_button.place(relx=0.5, rely=0.95, anchor='center')

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.scheduler.create_schedule(file_path)
                messagebox.showinfo("Success", "The schedule has been successfully created.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def open_settings(self):
        about_window = Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")  # Adjust the size as needed
        about_text = "Upload your excel containing list of students and their courses and be able to download the deferred exam schedule for this term."
        tk.Label(about_window, text="About This App", font=('Helvetica', 12, 'bold')).pack(pady=10)
        tk.Label(about_window, text=about_text, wraplength=250).pack(pady=10)

    def get_title(self):
        return self._title

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

if __name__ == "__main__":
    root = tk.Tk()
    scheduler = Scheduler()  # Assuming you have a Scheduler class to import
    app = UI(root, scheduler)
    root.mainloop()