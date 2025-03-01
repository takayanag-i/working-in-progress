from cruds.schedule.interface import ScheduleRepository
from src.models.schedule import ScheduleSchema
import json
import os


class ScheduleRepositoryMock(ScheduleRepository):
    def find_by_ttid(self, ttid: str) -> ScheduleSchema:
        file_path = os.path.join(os.path.dirname(__file__), '../resources/sample01/schedule_schema.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

            return ScheduleSchema(**data)
