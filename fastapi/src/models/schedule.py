from pydantic import BaseModel, ConfigDict, Field
from typing import List


class Slot(BaseModel):
    day: str
    available: bool
    am_periods: int = Field(None, alias="amPeriods")
    pm_periods: int = Field(None, alias="pmPeriods")

    model_config = ConfigDict(populate_by_name=True)


class ScheduleSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    slots: List[Slot]
    max_periods: int = Field(None, alias="maxPeriods")

    model_config = ConfigDict(populate_by_name=True)
