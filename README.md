# COMP4560-Deferred Exam Scheduler

## Introduction
The Deferred Exam Scheduler is an application designed to streamline the process of scheduling deferred exams for professors and educational administrators. By allowing the upload of student information, the application automates the creation of a schedule for all deferred exams, efficiently managing time slots and resources.

## Features
- **Automated Scheduling:** Automatically generate exam schedules based on student information.
- **Excel Upload:** Professors can upload student data through an Excel file, making it easy to integrate with existing records.
- **Conflict Resolution:** The app identifies and resolves scheduling conflicts to ensure no student is double-booked.
- **Customizable Settings:** Users can set preferences for exam times, durations, and locations.
- **Export Functionality:** Export the finalized exam schedule back to Excel or PDF for easy distribution and printing.

## Getting Started

### Prerequisites
- Python 3.x
- Tkinter (usually comes with Python)
- Pandas library for handling Excel files
- Openpyxl library for .xlsx file support

### Installation
1. Clone the repository to your local machine: git clone https://github.com/zacKolton/COMP4560-deferred-exam-project.git
2. Navigate to the cloned directory: cd Deferred-Exam-Scheduler3.
3. Install the required Python packages: pip install pandas openpyxl

### Running the Application
To start the application, run: python main.py

Follow the on-screen instructions to upload student data and generate the exam schedule.

## Usage
1. **Uploading Data:** Click the "Upload Excel File" button and select your Excel file containing the student information.
2. **Generating Schedule:** The app will process the uploaded file and automatically generate a deferred exam schedule.
3. **Exporting Schedule:** Save the generated schedule by clicking the "Export" button and choosing your preferred format.
