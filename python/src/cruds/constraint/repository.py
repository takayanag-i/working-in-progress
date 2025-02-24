from azure.cosmos import CosmosClient

from .interface import ConstraintRepository

from typing import List, Dict, Optional


class ConstraintRepositoryImpl(ConstraintRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self) -> Optional[List[Dict]]:
        pass
