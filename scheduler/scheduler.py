import pandas as pd
import numpy as np
import math

class Scheduler:
    def __init__(self):
        #self.in_csv = pd.read_excel("../data/InputData.xlsx")
        self.in_csv = None

        self.in_rooms = {
            "Armes 200": 100,
            "Armes 111": 35,
            "Armes 204": 85,
            "Armes 201": 52,
            "Armes 205": 52,
            "Armes 208": 85,
        }

        self.deferral_rate = 0.1

        self.exams_per_day = 3
        self.slot_names = {
            0: "Morning",
            1: "Afternoon",
            2: "Evening",
            3: "Night"
        }

    def index_to_timeslot(self, slot_index):
        day = math.floor(slot_index / self.exams_per_day)
        time_period = slot_index % self.exams_per_day
        period_name = self.slot_names[time_period]
        time_slot = f"Day: {day}, {period_name}"
        return time_slot

    def create_json_course_data(self, student_header, course_header):
        ret_data = {}

        for course in self.in_csv[course_header].unique():
            students_in_course = self.in_csv[self.in_csv[course_header] == course][student_header].unique()

            ret_data[course] = {
                "students": len(students_in_course),
                "conflicts": [],
            }

            for student in students_in_course:
                conflicts = self.in_csv[(self.in_csv[student_header] == student) &
                                        (self.in_csv[course_header] != course)][course_header].unique()
                ret_data[course]['conflicts'].extend(conflicts)

            ret_data[course]['num_conflicts'] = len(ret_data[course]['conflicts'])

        return ret_data

    def dict_to_df_no_rooms(self, schedule_dict, course_dict):
        list_courses = [(key, value['courses']) for key, value in schedule_dict.items()]
        ret_df = pd.DataFrame(list_courses, columns=["Time Slot", "Courses"])
        ret_df = ret_df.explode("Courses").reset_index(drop=True)

        def add_expected_deferrals(course_name):
            return math.ceil(course_dict[course_name]['students'] * self.deferral_rate)

        ret_df['Expected Deferrals'] = ret_df['Courses'].apply(add_expected_deferrals)
        return ret_df

    def json_to_adj_list(self, course_dict):
        vertices = list(course_dict.keys())
        adj_list = [[] for _ in vertices]

        for key, value in course_dict.items():
            vertex = vertices.index(key)
            for conflict in value['conflicts']:
                adj_list[vertex].append(vertices.index(conflict))

        return adj_list

    def greedy_colouring(self, adj_list):
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
        name_index = {name: i for i, name in enumerate(course_dict.keys())}
        index_name = {index: name for name, index in name_index.items()}

        course_adj_list = self.json_to_adj_list(course_dict)

        graph_color = self.greedy_colouring(course_adj_list)

        schedule = self.color_to_schedule(graph_color, index_name, course_dict)

        return schedule

    def run(self):
        courses_json = self.create_json_course_data("PIDM", "COURSE_IDENTIFICATION")
        sorted_courses = dict(sorted(courses_json.items(), key=lambda item: item[1]['students'], reverse=True))

        gc_schedule = self.graph_coloring_schedule(sorted_courses)
        gc_dict = self.dict_to_df_no_rooms(gc_schedule, courses_json)
        gc_dict.to_excel('../data/Outputs/Graph Coloring.xlsx', index=False, sheet_name='Schedule')


# Example usage:
# scheduler = Scheduler()
# scheduler.run()
