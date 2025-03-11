from abc import ABC, abstractmethod
from typing import List, Optional
from models.constraint import ConstraintSchema


class ConstraintRepository(ABC):
    @abstractmethod
    def find_by_ttid(self) -> Optional[List[ConstraintSchema]]:
        pass
