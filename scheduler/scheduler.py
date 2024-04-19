import json
import re
import time
import pandas as pd
import numpy as np
import math
import os
import random
import heapq
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
    
    def index_to_timeslot_2(self, slotIndex,examsPerDay, slotNames):
        day = math.floor(slotIndex/examsPerDay)
        timePeriod = slotIndex%examsPerDay
        periodName = slotNames[timePeriod]
        timeSlot = f"Day: {day}, {periodName}"
        return timeSlot
    
    def set_ui(self, ui):
        # Assigns a UI object to the scheduler for updating progress
        self.ui = ui

    def remove_course_codes(self, course_header):
        ret_data = []

        for course in self.in_csv[course_header].unique():
            course_code_removed = re.sub(r'\d', '', course)
             
            ret_data.append(course_code_removed)

        return list(set(ret_data))
    
    def count_students_per_field(self, student_header, course_header):
        ret_data = {}

        for _, row in self.in_csv.iterrows():
            pidm = row[student_header]
            course_code = row[course_header]

            field = str(re.sub(r'\d', '', course_code))

            if field in ret_data:
                ret_data[field]["student_count"] += 1
            else:
                ret_data[field] = {"student_count": 1}
        
        return ret_data
    
    def create_json_course_data(self, df, studentHeader, courseHeader):
        retData = {}
        courses = df[courseHeader].unique()

        for course in courses:
            # Num students in course
            studentsInCourse = df[df[courseHeader] == course][studentHeader].unique()
            
            if len(course) == 8:
                subj = course[:4].upper()
                if subj == "MBIO":
                    subj = "BIOL"
                retData[course] = {
                    "students": len(studentsInCourse),
                    "conflicts": [],
                    "conflictsDict": {},
                    "year": int(course[4]),
                    "subject": subj,
                    "subjectYear": course[:5].upper()
                }
            elif len(course) == 7:
                retData[course] = {
                    "students": len(studentsInCourse),
                    "conflicts": [],
                    "conflictsDict": {},
                    "year": int(course[3]),
                    "subject": course[:3].upper(),
                    "subjectYear": course[:4].upper()
                }
            else:
                print("it's time to contact the developers again")
            for conflict in courses:
                if course != conflict: 
                    studentsInOtherCourse = df[df[courseHeader] == conflict][studentHeader].unique()
                    studentsInConflicts = set(studentsInOtherCourse) & set(studentsInCourse)
                    if (studentsInConflicts):
                        retData[course]['conflicts'].append(conflict)
                        retData[course]['conflictsDict'][conflict] = len(studentsInConflicts)

            retData[course]['numConflicts'] = len(retData[course]['conflictsDict'])
        return retData

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
            course_codes_removed = self.remove_course_codes("COURSE_IDENTIFICATION")
            fields_count = self.count_students_per_field("PIDM", "COURSE_IDENTIFICATION")
            
            # print(course_codes_removed)
            # print(json.dumps(fields_count, indent=4))
        else:
            print("Invalid Data")

    def box_score(self, inCourse, selectedBox, coursesJSON):
        if inCourse not in selectedBox['conflicts']:
            # highest score 
            return 1000
        else:
            score = 0
            for course in selectedBox['scheduled']:
                if inCourse in coursesJSON[course]['conflicts']:
                    courseScore = -10
                    if coursesJSON[inCourse]['subjectYear'] == coursesJSON[course]['subjectYear']:
                        courseScore = courseScore - math.pow(20 - coursesJSON[inCourse]['year'], 1)
                    else:
                        courseScore = courseScore - math.pow(20 - coursesJSON[inCourse]['year'] - coursesJSON[course]['year'], 1)/2
                        if coursesJSON[inCourse]['subject'] == coursesJSON[course]['subject']:
                            courseScore = courseScore - 5
                    courseScore = courseScore*coursesJSON[inCourse]['conflictsDict'][course]
                    score += courseScore
            return score
        
    def find_random_max_box(self, boxScores):
        maxScore = max(boxScores.values())
        maxBoxes = [box for box, score in boxScores.items() if score == maxScore]
        return random.choice(maxBoxes)

    def add_conflicts_in_box(self, courses, box):
        for course in box['scheduled']:
            conflicts = list(set(courses[course]['conflicts']) & set(box['scheduled']))
            if len(conflicts):
                box['conflictsInSchedule'][course] = conflicts
                box['numConflicts'] += len(conflicts)

    def fill_boxes(self, courses, numBoxes):
        schedule1 = {f'{self.index_to_timeslot_2(i, 3, self.slot_names)}': {'scheduled': [], 'conflicts': [], 'conflictsInSchedule': {}, 'numConflicts': 0} for i in range(numBoxes)}

        for course_id, course_info in courses.items():
            boxScores = {box_id: self.box_score(course_id, box, courses) for box_id, box in schedule1.items()}
            targetBoxID = self.find_random_max_box(boxScores)

            schedule1[targetBoxID]['scheduled'].append(course_id)
            schedule1[targetBoxID]['conflicts'] = list(set(schedule1[targetBoxID]['conflicts']) | set(course_info['conflicts']))        
            
        for _, box in schedule1.items():
            self.add_conflicts_in_box(courses, box)
            del box['conflicts']

        return schedule1
    
    def sum_conflicts(self, boxes):
        totalConflicts = 0
        for box in boxes.values():
            totalConflicts += box['numConflicts']
        return totalConflicts
    
    def find_best_boxes(self, courseDict, numBoxes, runs=2000):
        minHeap = []

        for i in range(runs):
            boxes = self.fill_boxes(courseDict, numBoxes)
            totalConflicts = self.sum_conflicts(boxes)
            
            if len(minHeap) < 3:
                heapq.heappush(minHeap, (-totalConflicts, i, boxes)) 
            else:
                heapq.heappushpop(minHeap, (-totalConflicts, i, boxes))  

        return [heapq.heappop(minHeap)[2] for _ in range(len(minHeap))][::-1]
    
    def dict_to_df(self, scheduleDict, coursesJSON):
        listCourses = [(key, value['scheduled']) for key,value in scheduleDict.items()]
        retDf = pd.DataFrame(listCourses, columns=["Time Slot", "Courses"])
        retDf = retDf.explode("Courses").reset_index(drop=True)

        conflictsDict = {}
        for box in scheduleDict.values():
            if box['conflictsInSchedule']:
                for course, conflicts in box['conflictsInSchedule'].items():
                    courseConflicts = {}
                    for conflict in conflicts: 
                        if coursesJSON[course]['conflictsDict'][conflict]:
                            courseConflicts[conflict] = coursesJSON[course]['conflictsDict'][conflict]
                    conflictsDict[course] = courseConflicts

        retDf['Conflict Details'] = retDf['Courses'].map(lambda x: conflictsDict.get(x, {}))
        
        return retDf
        
    def run(self, constraint):
        constraint = constraint*3
        # Main execution method for scheduling
        self.ui.update_progress("Extracting/processing data...\n(This may take a while)")
        if self.in_csv is not None:
            if "PIDM" in self.in_csv.columns and "COURSE_IDENTIFICATION" in self.in_csv.columns:
                current_timestamp = int(time.time())
                courses_json = self.create_json_course_data(self.in_csv, "PIDM", "COURSE_IDENTIFICATION")
                sorted_courses = dict(sorted(courses_json.items(), key=lambda item: item[1]['students'], reverse=True))

                self.ui.update_progress("Analyzing/scheduling...")
                if (constraint > 0):
                    output = self.find_best_boxes(sorted_courses, constraint)
                    
                    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
                    i = 0

                    for schedule in output:
                        df = self.dict_to_df(schedule, sorted_courses)
                        output_file = os.path.join(downloads_path, f"Schedule_Days_{constraint}_{i}_{current_timestamp}.xlsx")
                        df.to_excel(output_file, index=False, sheet_name='Schedule')
                        i +=1
                else:
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