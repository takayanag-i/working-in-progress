from abc import ABC, abstractmethod
from typing import List, Optional

from models.homeroom import Homeroom


class HomeroomRepository(ABC):
    @abstractmethod
    def find_by_ttid(self, ttid: str) -> Optional[List[Homeroom]]:
        pass
