from abc import ABC, abstractmethod
from typing import Optional

from models.homeroom import HomeroomSchema


class HomeroomRepository(ABC):
    @abstractmethod
    def find_by_ttid(self, ttid: str) -> Optional[HomeroomSchema]:
        pass
