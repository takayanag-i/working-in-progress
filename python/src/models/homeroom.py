from pydantic import BaseModel
from typing import List


class Schedule(BaseModel):
    day: str
    lastPeriod: int


class Homeroom(BaseModel):
    name: str
    schedule: List[Schedule]


class HomeroomSchema(BaseModel):
    id: str
    docType: str
    ttid: str
    homerooms: List[Homeroom]
