from azure.cosmos import CosmosClient

from .interface import CurriculumRepository

from typing import List, Dict, Optional


class CurriculumRepositoryImpl(CurriculumRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_id(self) -> Optional[List[Dict]]:
        pass
