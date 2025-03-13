from pydantic import BaseModel, ConfigDict, Field
from typing import List


class Day(BaseModel):
    day: str
    last_period: int = Field(..., alias="lastPeriod")

    model_config = ConfigDict(populate_by_name=True)


class Homeroom(BaseModel):
    homeroom: str
    days: List[Day]

    model_config = ConfigDict(populate_by_name=True)


class HomeroomSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    homerooms: List[Homeroom]

    model_config = ConfigDict(populate_by_name=True)
