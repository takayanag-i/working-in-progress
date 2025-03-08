from pydantic import BaseModel, ConfigDict, Field


class ConstraintSchema(BaseModel):
    id: str
    doc_type: str = Field(..., alias="docType")
    ttid: str
    constraint_type: str = Field(..., alias="constraintType")
    parameters: dict[str, str | int]

    model_config = ConfigDict(populate_by_name=True)
