from pydantic import BaseModel
from typing import List, Dict, Optional


class CourseDetail(BaseModel):
    instructors: List[str]
    credits: int


class AnualData(BaseModel):
    H: Optional[List[str]]
    D: Optional[List[str]]
    P: Optional[List[int]]
    C: Optional[List[str]]
    I: Optional[List[str]]
    periods: Optional[Dict[str, Dict[str, List[int]]]]
    curriculums: Optional[Dict[str, List[List[List[str]]]]]
    course_details: Optional[Dict[str, CourseDetail]]
