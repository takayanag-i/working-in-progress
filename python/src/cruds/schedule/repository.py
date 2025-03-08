from azure.cosmos import CosmosClient
from models.schedule import ScheduleSchema
from .interface import ScheduleRepository
from typing import Optional


class ScheduleRepositoryImpl(ScheduleRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self) -> Optional[ScheduleSchema]:
        pass
