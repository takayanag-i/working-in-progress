from cruds.curriculum.interface import CurriculumRepository
from models.curriculum import CurriculumSchema
import json
import os


class CurriculumRepositoryMock(CurriculumRepository):
    def find_by_ttid(self, ttid: str) -> CurriculumSchema:
        file_path = os.path.join(os.path.dirname(__file__), '../resources/sample01/curriculum_schema.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

            return CurriculumSchema(**data)
