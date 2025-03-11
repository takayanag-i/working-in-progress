from abc import ABC, abstractmethod
from typing import Optional

from models.schedule import ScheduleSchema


class ScheduleRepository(ABC):
    @abstractmethod
    def find_by_ttid(self) -> Optional[ScheduleSchema]:
        pass
