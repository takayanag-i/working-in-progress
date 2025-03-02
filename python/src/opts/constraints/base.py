from abc import ABC, abstractmethod
from common.constants import ConstraintType
from opts.anual_model import AnualModel


class ConstraintBase(ABC):

    def __init__(self, constraint_type: ConstraintType):
        self.constraint_type = constraint_type

    @abstractmethod
    def apply(self, model: AnualModel) -> AnualModel:
        pass
