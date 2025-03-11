from azure.cosmos import CosmosClient
from models.constraint import ConstraintSchema
from .interface import ConstraintRepository
from typing import List, Optional


class ConstraintRepositoryImpl(ConstraintRepository):
    def __init__(self, cosmos: CosmosClient):
        self.cosmos = cosmos

    def find_by_ttid(self) -> Optional[List[ConstraintSchema]]:
        pass
