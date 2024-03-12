from app_logic.app import App
import tkinter as tk

def main():
    root = tk.Tk()
    app = App(root)
    app.startup()

if __name__ == "__main__":
    main()

