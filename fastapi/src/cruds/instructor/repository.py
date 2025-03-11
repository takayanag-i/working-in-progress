from azure.cosmos import CosmosClient

from .interface import InstructorRepository

from typing import List, Dict, Optional


class InstructorRepositoryImpl(InstructorRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self) -> Optional[List[Dict]]:
        pass
