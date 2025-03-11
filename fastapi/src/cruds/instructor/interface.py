from abc import ABC, abstractmethod
from typing import List, Optional

from models.instructor import Instructor


class InstructorRepository(ABC):
    @abstractmethod
    def find_by_ttid(self) -> Optional[List[Instructor]]:
        pass
