import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk

from scheduler.scheduler import Scheduler

class UI:
    def __init__(self, master, scheduler):
        # Initialize the main UI window
        self.root = master
        self.scheduler = Scheduler()  # Reference to the scheduler object
        self._title = "Deferred Exam Scheduler"
        self._width = 700  # Width of the window
        self._height = 400  # Height of the window

        # Set the title and size of the window
        self.root.title(self._title)
        self.root.geometry(f"{self._width}x{self._height}")

        try:
            # Load and resize the background image
            pil_image = Image.open("./branding/background.jpg")
            resized_image = pil_image.resize((self._width, self._height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)

            # Set the resized image as the background
            self.background_label = tk.Label(self.root, image=self.photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading the background image: {e}")
            self.root.configure(bg='gray')  # Set a default background color if the image fails to load

        # Create and configure the upload button
        self.upload_button = tk.Button(self.root, text="Upload Schedule Data", command=self.upload_file)
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

        self.run_scheduler_button = tk.Button(self.root, text="Run Scheduler", command=self.scheduler.run)
        self.run_scheduler_button.configure(
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

        self.run_scheduler_button.place(x=500, y=200, anchor='center')

        # Create and configure the settings button
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
        # Open a file dialog to select an Excel file and create a schedule
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.scheduler.set_input_data(file_path)
                messagebox.showinfo("Success", "The file has been successfully created.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def open_settings(self):
        # Open a new window showing the "About" information
        about_window = Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")  # Size of the about window
        about_text = "Upload your excel containing list of students and their courses and be able to download the deferred exam schedule for this term."
        tk.Label(about_window, text="About This App", font=('Helvetica', 12, 'bold')).pack(pady=10)
        tk.Label(about_window, text=about_text, wraplength=250).pack(pady=10)

    def get_title(self):
        # Return the title of the app
        return self._title

    def get_width(self):
        # Return the width of the app window
        return self._width

    def get_height(self):
        # Return the height of the app window
        return self._height

if __name__ == "__main__":
    root = tk.Tk()
    scheduler = Scheduler()  # Create an instance of the Scheduler class
    app = UI(root, scheduler)  # Create an instance of the UI class
    root.mainloop()