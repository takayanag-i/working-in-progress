from azure.cosmos import CosmosClient

from .interface import HomeroomRepository

from typing import List, Dict, Optional


class HomeroomRepositoryImpl(HomeroomRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self, ttid: str) -> Optional[List[Dict]]:
        pass
