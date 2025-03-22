from abc import ABC, abstractmethod
from opts.anual_model import AnualModel


class ConstraintBase(ABC):
    @abstractmethod
    def apply(self, model: AnualModel) -> AnualModel:
        raise NotImplementedError()
