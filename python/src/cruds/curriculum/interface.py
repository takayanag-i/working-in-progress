from abc import ABC, abstractmethod
from typing import List, Optional

from models.curriculum import Curriculum


class CurriculumRepository(ABC):
    @abstractmethod
    def find_by_id(self) -> Optional[List[Curriculum]]:
        pass
