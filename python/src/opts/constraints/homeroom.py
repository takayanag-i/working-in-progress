from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import pulp


class HomeroomConstraint(ConstraintBase):
    """
    A concrete implementation of the ConstraintBase class for homeroom constraints.
    """

    def __init__(self, id: str = None):
        """
        Initializes a new instance of the HomeroomConstraint class.

        Args:
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        super().__init__(ConstraintType.HOMEROOM, id)

    def apply(self, model: AnualModel):
        """
        Applies the homeroom constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        for h in model.dto.homeroom_list:
            for d in model.dto.day_of_week:
                for p in model.dto.schedule[h][d]:
                    model.prob += pulp.lpSum(
                        [model.x[h, d, p, c] for block in model.dto.curriculum_dict[h] for lane in block for c in lane]
                    ) >= 1
