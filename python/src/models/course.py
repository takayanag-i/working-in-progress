from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class CourseDetail(BaseModel):
    instructor: str
    room: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class Course(BaseModel):
    name: str
    subject: str
    credits: int
    details: List[CourseDetail]

    model_config = ConfigDict(populate_by_name=True)


class CourseSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    courses: List[Course]

    model_config = ConfigDict(populate_by_name=True)
