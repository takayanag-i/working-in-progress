from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel


class TeacherConstraint(ConstraintBase):
    """
    A concrete implementation of the ConstraintBase class for teacher constraints.
    """

    def __init__(self, id: str = None):
        """
        Initializes a new instance of the Teacher class.

        Args:
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        super().__init__(ConstraintType.TEACHER, id)

    def apply(self, model: AnualModel):
        """
        Applies the teacher constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        for d in model.dto.day_of_week:
            for p in range(1, 8):
                for t in model.dto.teacher_list:
                    model.prob += model.y[d, p, t] <= 1
