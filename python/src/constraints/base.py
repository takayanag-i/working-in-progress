from abc import ABC, abstractmethod
from python.src.opts.anual_solver import AnualSolver
import uuid


class ConstraintBase(ABC):
    def __init__(self, constraint_type: str, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.constraint_type = constraint_type

    @abstractmethod
    def apply(self, model: AnualSolver):
        """ 各制約クラスでオーバーライドする """
        pass
