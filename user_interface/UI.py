import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel
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

        # UI window configuration
        self._title = "Deferred Exam Scheduler"
        self._width = 700  # Window width
        self._height = 400  # Window height

        # Set window title and size
        self.root.title(self._title)
        self.root.geometry(f"{self._width}x{self._height}")

        # Try to load and set the background image
        try:
            pil_image = Image.open("./branding/background.jpg")
            resized_image = pil_image.resize((self._width, self._height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.background_label = tk.Label(self.root, image=self.photo)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading the background image: {e}")
            self.root.configure(bg='gray')  # Fallback background color

        # Upload button configuration and placement
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

        # Button to initiate the scheduling process
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

        # Text widget for displaying progress and errors
        self.progress_text = tk.Text(self.root, height=4, width=50)
        self.progress_text.place(x=350, y=300, anchor='center')
        self.progress_text.tag_configure('error', foreground='red')

        # Settings button with a gear icon
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

        # Label explaining the dropdown
        self.constraint_label = tk.Label(self.root, text="Select the maximum number of days you want to schedule your exams within: \n[DEFAULT] '0' represents the scheduler will create a conflict free schedule. ", font=('Helvetica', 10))
        self.constraint_label.place(x=self._width // 2, y=self._height // 2 - 80, anchor='center')

        # Dropdown for selecting the constraint number
        self.constraint_var = tk.IntVar(self.root)
        self.constraint_combobox = ttk.Combobox(self.root, textvariable=self.constraint_var, values=[i for i in range(11)], width=10)
        self.constraint_combobox.set(0)  # Default value
        self.constraint_combobox.place(x=self._width // 2, y=self._height // 2 - 50, anchor='center')

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

    def run_scheduler(self):
        # Get the value from the combobox and start the scheduler
        constraint = self.constraint_var.get()
        self.update_progress("Starting scheduling process...")
        threading.Thread(target=self.scheduler.run, args=[constraint]).start()

    def open_settings(self):
        # Open a new window for settings or about info
        about_window = Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("300x200")
        about_text = "Upload your excel containing list of students and their courses and be able to download the deferred exam schedule for this term."
        tk.Label(about_window, text="About This App", font=('Arial', 12, 'bold')).pack(pady=10)
        tk.Label(about_window, text=about_text, wraplength=250).pack(pady=10)

    def get_title(self):
        return self._title

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height