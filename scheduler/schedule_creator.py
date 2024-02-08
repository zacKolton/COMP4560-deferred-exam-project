import pandas as pd

class ScheduleCreator:
    def __init__(self):
        pass 

    ## TODO: Implement
    def create_schedule(self, file_path):
        data = pd.read_excel(file_path)

        return data