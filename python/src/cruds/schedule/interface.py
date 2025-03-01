from abc import ABC, abstractmethod
from typing import List, Optional

from models.schedule import Schedule


class ScheduleRepository(ABC):
    @abstractmethod
    def find_by_ttid(self) -> Optional[List[Schedule]]:
        pass
