from pydantic import BaseModel
from typing import List


class Day(BaseModel):
    day: str
    lastPeriod: int


class Homeroom(BaseModel):
    name: str
    schedule: List[Day]


class HomeroomSchema(BaseModel):
    id: str
    docType: str
    ttid: str
    homerooms: List[Homeroom]
