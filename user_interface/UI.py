import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, OptionMenu
from PIL import Image, ImageTk
import threading

# Assume Scheduler is defined in scheduler.scheduler
from scheduler.scheduler import Scheduler

class UI:
    def __init__(self, master, scheduler):
        # Initialize the main UI window and set up the scheduler
        self.root = master
        self.scheduler = scheduler
        self.scheduler.set_ui(self)  # Link the UI to the scheduler for callbacks

        # The default number of exam days from the Scheduler
        self.num_exam_days = tk.IntVar(value=scheduler.default_num_exam_days)

        # Dropdown menu for selecting the number of exam days
        self.days_dropdown = tk.OptionMenu(
            self.root, 
            self.num_exam_days, 
            *range(1, 11)  # Creates options from 1 to 10
        )

        # UI window configuration
        self._title = "Deferred Exam Scheduler"
        self._width = 700  # Window width
        self._height = 400  # Window height

        # Set window title and size
        self.root.title(self._title)
        self.root.geometry(f"{self._width}x{self._height}")

        # Background Image
        try:
            pil_image = Image.open("./branding/background.jpg")
            resized_image = pil_image.resize((self._width, self._height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.background_label = tk.Label(self.root, image=self.photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading the background image: {e}")
            self.root.configure(bg='gray')  # Fallback background color

        # Upload button
        self.upload_button = tk.Button(self.root, text="Upload Schedule Data", command=self.upload_file)
        self.upload_button.configure(
            font=('Arial', 12, 'bold'), 
            fg='black', 
            bg='#0078D7', 
            activebackground='#0053ba', 
            activeforeground='black', 
            bd=2, 
            relief='raised', 
            padx=10, 
            pady=5
        )
        self.upload_button.place(x=self._width // 2 - 75, y=self._height // 2, anchor='center')

        # Run scheduler button
        self.run_scheduler_button = tk.Button(self.root, text="Run Scheduler", command=self.run_scheduler)
        self.run_scheduler_button.configure(
            font=('Arial', 12, 'bold'), 
            fg='black', 
            bg='#0078D7', 
            activebackground='#0053ba', 
            activeforeground='black', 
            bd=2, 
            relief='raised', 
            padx=10, 
            pady=5
        )
        self.run_scheduler_button.place(x=self._width // 2 + 75, y=self._height // 2, anchor='center')


        # Dropdown Widget
        self.days_dropdown.config(width=15, font=('Arial', 10))
        self.days_dropdown.place(x=self._width // 2 - 75, y=self._height // 2 - 50, anchor='center')

        # Message Widget
        self.progress_text = tk.Text(self.root, height=4, width=50)
        self.progress_text.place(x=350, y=300, anchor='center')
        self.progress_text.tag_configure('error', foreground='red')

        # Settings button
        self.settings_button = tk.Button(self.root, text='⚙', command=self.open_settings)
        self.settings_button.configure(
            font=('Arial', 14, 'bold'), 
            fg='black', 
            bg='gray', 
            bd=0, 
            relief='flat', 
            highlightthickness=0
        )
        self.settings_button.place(relx=0.5, rely=0.95, anchor='center')

    def update_progress(self, message, error=False):
        # Insert message into the Text widget and scroll to the end
        self.progress_text.insert(tk.END, message + "\n")
        if error:
            start_index = self.progress_text.index("end-1c linestart")
            end_index = self.progress_text.index("end-1c")
            self.progress_text.tag_add('error', start_index, end_index)
        self.progress_text.see(tk.END)

    def upload_file(self):
        # File dialog to select the Excel file for scheduling
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            try:
                self.scheduler.set_input_data(file_path)
                self.update_progress("Uploaded schedule")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def set_num_exams(self, selection):
        self.scheduler.selected_num_exam_days = selection

    def run_scheduler(self):
        # Start the scheduler in a separate thread to prevent UI freezing
        self.scheduler.exams_per_day = self.num_exam_days.get()
        self.update_progress("Starting scheduling process...")
        threading.Thread(target=self.scheduler.run).start()

    def open_settings(self):
        # Open a new window for settings or about info
        about_window = Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")
        about_text = "Upload your excel containing list of students and their courses and be able to download the deferred exam schedule for this term."
        tk.Label(about_window, text="About This App", font=('Helvetica', 12, 'bold')).pack(pady=10)
        tk.Label(about_window, text=about_text, wraplength=250).pack(pady=10)

    def get_title(self):
        return self._title

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

