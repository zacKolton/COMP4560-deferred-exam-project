# COMP4560-Deferred Exam Scheduler

## Project Overview
The Deferred Exam Scheduler is a GUI application designed to automate the process of scheduling deferred exams. It ensures that no student is scheduled to take two exams at the same time, thus eliminating conflicts. This is achieved by employing a graph coloring algorithm to assign time slots to exams while managing conflicts.

## Installation
Before you can run the application, ensure you have the following prerequisites installed:
- Python 3
- Tkinter (usually comes with Python)
- PIL (Python Imaging Library)
- pandas
- numpy

To install the necessary Python packages, run: ``pip install -r requirements.txt``

## How to Use
1. Launch the application by running `main.py`.
2. Use the "Upload Schedule Data" button to select and upload the Excel file containing the exam data.
3. Click "Run Scheduler" to process the uploaded data and generate the schedule.
4. Access the schedule in the specified download location, which will be indicated in the application upon completion.


## Features
- Upload exam data through a user-friendly graphical interface.
- Automatic conflict resolution between different exams based on shared students.
- Efficient scheduling using a greedy graph coloring algorithm.
- Output the final exam schedule in an Excel file.


## Directory Structure
- `main.py`: The entry point of the application.
- `scheduler/`: Contains the `Scheduler` class that handles scheduling logic.
- `user_interface/`: Contains the `UI` class that handles the graphical user interface.
- `branding/`: Contains the branding assets like background images and logos.
- `requirements.txt`: Lists all the Python dependencies for the project.
- `LICENSE`: The license file.
