from abc import ABC, abstractmethod
from typing import List, Optional

from models.course import Course


class CourseRepository(ABC):
    @abstractmethod
    def find_by_course_id(self) -> Optional[List[Course]]:
        pass
