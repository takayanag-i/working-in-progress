from pydantic import BaseModel, Field, ConfigDict
from typing import List


class Lane(BaseModel):
    courses: List[str]

    model_config = ConfigDict(populate_by_name=True)


class Block(BaseModel):
    name: str
    lanes: List[Lane]

    model_config = ConfigDict(populate_by_name=True)


class Curriculum(BaseModel):
    homeroom: str
    blocks: List[Block]

    model_config = ConfigDict(populate_by_name=True)


class CurriculumSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    curriculums: List[Curriculum]

    model_config = ConfigDict(populate_by_name=True)
