import time
import pandas as pd
import numpy as np
import math
import os
from datetime import datetime

class Scheduler:
    def __init__(self):
        # Input data placeholder for exam data, initially set to None
        self.in_csv = None

        # Room information: room name mapped to its capacity
        self.in_rooms = {
            "Armes 200": 100,
            "Armes 111": 35,
            "Armes 204": 85,
            "Armes 201": 52,
            "Armes 205": 52,
            "Armes 208": 85,
        }

        # Percentage of students expected to defer their exams
        self.deferral_rate = 0.1

        # Number of exam slots available per day
        self.exams_per_day = 3

        # Mapping slot indexes to human-readable time periods
        self.slot_names = {
            0: "Morning",
            1: "Afternoon",
            2: "Evening",
            3: "Night"
        }

    def index_to_timeslot(self, slot_index):
        # Converts a numerical slot index to a readable timeslot string
        day = math.floor(slot_index / self.exams_per_day)
        time_period = slot_index % self.exams_per_day
        period_name = self.slot_names[time_period]
        time_slot = f"Day: {day}, {period_name}"
        return time_slot
    
    def set_ui(self, ui):
        # Assigns a UI object to the scheduler for updating progress
        self.ui = ui

    def create_json_course_data(self, student_header, course_header):
        # Generates a JSON-like structure containing course data and conflicts
        ret_data = {}

        # Loop through each unique course in the dataset
        for course in self.in_csv[course_header].unique():
            students_in_course = self.in_csv[self.in_csv[course_header] == course][student_header].unique()

            # Store student count and initialize conflicts list for each course
            ret_data[course] = {
                "students": len(students_in_course),
                "conflicts": [],
            }

            # Identify conflicts for each student in the course
            for student in students_in_course:
                conflicts = self.in_csv[(self.in_csv[student_header] == student) &
                                        (self.in_csv[course_header] != course)][course_header].unique()
                ret_data[course]['conflicts'].extend(conflicts)

            # Count the total number of conflicts for the course
            ret_data[course]['num_conflicts'] = len(ret_data[course]['conflicts'])

        return ret_data

    def dict_to_df_no_rooms(self, schedule_dict, course_dict):
        # Converts the scheduling dictionary to a DataFrame excluding room assignments
        list_courses = [(key, value['courses']) for key, value in schedule_dict.items()]
        ret_df = pd.DataFrame(list_courses, columns=["Time Slot", "Courses"])
        ret_df = ret_df.explode("Courses").reset_index(drop=True)

        def add_expected_deferrals(course_name):
            # Calculates expected deferrals for a course based on deferral rate
            return math.ceil(course_dict[course_name]['students'] * self.deferral_rate)

        ret_df['Expected Deferrals'] = ret_df['Courses'].apply(add_expected_deferrals)
        return ret_df

    def json_to_adj_list(self, course_dict):
        # Converts course data into an adjacency list representing course conflicts
        vertices = list(course_dict.keys())
        adj_list = [[] for _ in vertices]

        for key, value in course_dict.items():
            vertex = vertices.index(key)
            for conflict in value['conflicts']:
                adj_list[vertex].append(vertices.index(conflict))

        return adj_list

    def greedy_colouring(self, adj_list):
        # Implements a greedy coloring algorithm to assign timeslots to courses
        num_vertices = len(adj_list)
        result = [-1] * num_vertices

        result[0] = 0
        available = [False] * num_vertices

        for vertex in range(1, num_vertices):
            for i in adj_list[vertex]:
                if result[i] != -1:
                    available[result[i]] = True

            time_slot = 0
            while time_slot < num_vertices:
                if not available[time_slot]:
                    break
                time_slot += 1

            result[vertex] = time_slot
            for i in adj_list[vertex]:
                if result[i] != -1:
                    available[result[i]] = False

        return result

    def color_to_schedule(self, graph_color, index_name, course_dict):
        # Converts graph coloring result into a schedule dictionary
        ret_dict = {}
        for vertex, color in enumerate(graph_color):
            time_slot = self.index_to_timeslot(color)
            course_name = index_name[vertex]
            if time_slot in ret_dict:
                ret_dict[time_slot]['courses'].append(course_name)
                ret_dict[time_slot]['num_students'] += math.ceil(
                    course_dict[course_name]['students'] * self.deferral_rate)
            else:
                ret_dict[time_slot] = {
                    'courses': [course_name],
                    'num_students': math.ceil(course_dict[course_name]['students'] * self.deferral_rate)
                }
        return ret_dict

    def graph_coloring_schedule(self, course_dict):
        # Main function to create a schedule using graph coloring
        name_index = {name: i for i, name in enumerate(course_dict.keys())}
        index_name = {index: name for name, index in name_index.items()}

        course_adj_list = self.json_to_adj_list(course_dict)
        graph_color = self.greedy_colouring(course_adj_list)
        schedule = self.color_to_schedule(graph_color, index_name, course_dict)

        return schedule
    
    def set_input_data(self, inputData):
        # Sets the input data for the scheduler from a file
        if inputData is not None and inputData != "":
            self.in_csv = pd.read_excel(inputData)
        else:
            print("Invalid Data")

    def run(self):
        # Main execution method for scheduling
        self.ui.update_progress("Extracting/processing data...\n(This may take a while)")
        if self.in_csv is not None:
            if "PIDM" in self.in_csv.columns and "COURSE_IDENTIFICATION" in self.in_csv.columns:
                current_timestamp = int(time.time())
                courses_json = self.create_json_course_data("PIDM", "COURSE_IDENTIFICATION")
                sorted_courses = dict(sorted(courses_json.items(), key=lambda item: item[1]['students'], reverse=True))

                self.ui.update_progress("Analyzing/scheduling...")
                gc_schedule = self.graph_coloring_schedule(sorted_courses)

                gc_dict = self.dict_to_df_no_rooms(gc_schedule, courses_json)

                downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
                output_file = os.path.join(downloads_path, f"Deferred_Exam_Schedule_{current_timestamp}.xlsx")

                gc_dict.to_excel(output_file, index=False, sheet_name='Schedule')
                self.ui.update_progress(f"Done! Downloaded at: {output_file}")
                print(f"Schedule saved to {output_file}")
            else:
                print("Required columns are missing in the input data.")
                self.ui.update_progress("Required columns are missing in the input data.\nPlease check the excel file and re-upload!", error=True)
        else:
            print("Missing data. Please upload the data file.")