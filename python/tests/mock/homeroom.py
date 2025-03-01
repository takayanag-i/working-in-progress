from cruds.homeroom.interface import HomeroomRepository
from models.homeroom import HomeroomSchema
import json
import os


class HomeroomRepositoryMock(HomeroomRepository):
    def find_by_ttid(self, ttid: str) -> HomeroomSchema:
        file_path = os.path.join(os.path.dirname(__file__), '../resources/sample01/homeroom_schema.json')

        with open(file_path, 'r') as file:
            data = json.load(file)

            return HomeroomSchema(**data)
