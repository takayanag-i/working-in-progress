from pydantic import BaseModel, Field
from typing import List


class Slot(BaseModel):
    day: str
    last_period: int = Field(..., alias="lastPeriod")

    class Config:
        populate_by_name = True


class Homeroom(BaseModel):
    name: str
    slots: List[Slot] = Field(..., alias="slots")

    class Config:
        populate_by_name = True


class HomeroomSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    homerooms: List[Homeroom]

    class Config:
        populate_by_name = True
