from azure.cosmos import CosmosClient
from models.homeroom import HomeroomSchema
from .interface import HomeroomRepository
from typing import Optional


class HomeroomRepositoryImpl(HomeroomRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self, ttid: str) -> Optional[HomeroomSchema]:
        pass
