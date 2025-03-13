from pydantic import BaseModel, ConfigDict, Field
from typing import List


class Day(BaseModel):
    name: str
    available: bool
    am_periods: int = Field(None, alias="amPeriods")
    pm_periods: int = Field(None, alias="pmPeriods")

    model_config = ConfigDict(populate_by_name=True)


class ScheduleSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    days: List[Day]
    max_periods: int = Field(None, alias="maxPeriods")

    model_config = ConfigDict(populate_by_name=True)
