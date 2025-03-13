from pydantic import BaseModel, ConfigDict, Field
from typing import List


class Day(BaseModel):
    day: str
    period: int
    available: bool

    model_config = ConfigDict(populate_by_name=True)


class Instructor(BaseModel):
    name: str
    discipline: str
    credits: int
    slots: List[Day]

    model_config = ConfigDict(populate_by_name=True)


class InstructorSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    instructors: List[Instructor]

    model_config = ConfigDict(populate_by_name=True)
