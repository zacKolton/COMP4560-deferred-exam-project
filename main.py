import tkinter as tk

from scheduler.scheduler import Scheduler
from user_interface.UI import UI

def main():
    root = tk.Tk()
    scheduler = Scheduler()
    ui = UI(root, scheduler)
    root.mainloop()

if __name__ == "__main__":
    main()

