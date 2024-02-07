import tkinter as tk

from tkinter import filedialog, messagebox
import shutil
import os

from user_interface.UI import UI
from app_logic.app import App

def main():
    root = tk.Tk()
    app = App(None)
    app_user_interface = UI(root, app)
    app.ui = app_user_interface
    root.mainloop()

if __name__ == "__main__":
    main()


