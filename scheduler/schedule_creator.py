import pandas as pd
import numpy as np
import math

inCsv = pd.read_excel("../data/InputData.xlsx")

inRooms = {
    "Armes 200": 100,
    "Armes 111": 35,
    "Armes 204": 85,
    "Armes 201": 52,
    "Armes 205": 52,
    "Armes 208": 85,
}

deferralRate = 0.1

examsPerDay = 3
slotNames = {
    0: "Morning",
    1: "Afternoon",
    2: "Evening",
    3: "Night"
}

def index_to_timeslot(slotIndex,examsPerDay, slotNames):
    day = math.floor(slotIndex/examsPerDay)
    timePeriod = slotIndex%examsPerDay
    periodName = slotNames[timePeriod]
    timeSlot = f"Day: {day}, {periodName}"
    return timeSlot

def create_JSON_course_data(df, studentHeader, courseHeader):
    retData = {}

    for course in df[courseHeader].unique():
        studentsInCourse = df[df[courseHeader] == course][studentHeader].unique()
        
        retData[course] = {
            "students": len(studentsInCourse),
            "conflicts": [],
        }

        for student in studentsInCourse: 
            conflicts = df[(df[studentHeader] == student) & (df[courseHeader] != course)][courseHeader].unique()
            retData[course]['conflicts'].extend(conflicts)
        
        retData[course]['numConflicts'] = len(retData[course]['conflicts'])


    return retData

def dict_to_df_no_rooms(scheduleDict, courseDict, deferralRate):
    listCourses = [(key, value['courses']) for key,value in scheduleDict.items()]
    retDf = pd.DataFrame(listCourses, columns=["Time Slot", "Courses"])
    retDf = retDf.explode("Courses").reset_index(drop=True)
    
    def addExpectedDeferrals(courseName, courseDict, deferralRate):
        return math.ceil(courseDict[courseName]['students']*deferralRate)
    
    retDf['Expected Deferrals'] = retDf['Courses'].apply(addExpectedDeferrals, args=(courseDict, deferralRate))
    return retDf


coursesJSON = create_JSON_course_data(inCsv, "PIDM", "COURSE_IDENTIFICATION")
sortedCourses = dict(sorted(coursesJSON.items(), key=lambda item: item[1]['students'], reverse=True))
rooms = {key: value for key, value in sorted(inRooms.items(), key=lambda item: item[1], reverse=True)}

def json_to_adj_list(courseDict, nameIndex):
    vertices = list(courseDict.keys())
    adjList = [[] for _ in vertices]

    for key, value in courseDict.items():
        vertex = nameIndex[key]
        for conflict in value['conflicts']:
            adjList[vertex].append(nameIndex[conflict])

    return adjList

def greedy_colouring(adjList):
    numVertices = len(adjList)
    result = [-1]*numVertices

    result[0] = 0

    available = [False]*numVertices

    for vertex in range(1, numVertices):
        
        for i in adjList[vertex]:
            if(result[i] != -1):
                available[result[i]] = True

        timeSlot = 0
        while timeSlot < numVertices:
            if available[timeSlot] == False:
                break

            timeSlot += 1

        result[vertex] = timeSlot

        for i in adjList[vertex]:
            if result[i] != -1:
                available[result[i]] = False

    return result


def color_to_schedule(graphColor, indexName, courseDict, deferralRate):
    numVertices = len(graphColor)
    retDict = {}
    for vertex in range(numVertices):
        timeSlot = index_to_timeslot(graphColor[vertex], examsPerDay, slotNames)
        courseName = indexName[vertex]
        if timeSlot in retDict:
            retDict[timeSlot]['courses'].append(courseName)
            retDict[timeSlot]['numStudents'] += math.ceil(courseDict[courseName]['students']*deferralRate)
        else:
            retDict[timeSlot] = {
                'courses': [courseName],
                'numStudents': math.ceil(courseDict[courseName]['students']*deferralRate)
            }
    return retDict

def graph_coloring_schedule(courseDict, deferralRate):
    nameIndex = {name: i for i, name in enumerate(courseDict.keys())}
    indexName = {index: name for name, index in nameIndex.items()}

    courseAdjList = json_to_adj_list(courseDict, nameIndex)
    
    graphColor = greedy_colouring(courseAdjList)

    schedule = color_to_schedule(graphColor, indexName, courseDict, deferralRate)
    
    return schedule

gcSchedule = graph_coloring_schedule(sortedCourses, deferralRate)
gcDict = dict_to_df_no_rooms(gcSchedule, coursesJSON, deferralRate)
gcDict.to_excel('../data/Outputs/Graph Coloring.xlsx', index=False, sheet_name='Schedule')