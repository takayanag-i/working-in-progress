from abc import ABC, abstractmethod
from typing import List, Optional

from models.homeroom import Homeroom


class HomeroomRepository(ABC):
    @abstractmethod
    def find_by_ttid(self) -> Optional[List[Homeroom]]:
        pass
