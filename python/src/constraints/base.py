from abc import ABC, abstractmethod
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import uuid


class ConstraintBase(ABC):
    """
    Base class for all constraints.

    Attributes:
        id (str): Unique identifier for the constraint.
        constraint_type (ConstraintType): Type of the constraint.
    """

    def __init__(self, constraint_type: ConstraintType, id: str = None):
        """
        Initializes a new instance of the ConstraintBase class.

        Args:
            constraint_type (ConstraintType): Type of the constraint.
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        self.id = id or str(uuid.uuid4())
        self.constraint_type = constraint_type

    @abstractmethod
    def apply(self, model: AnualModel):
        """
        Applies the constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        pass
