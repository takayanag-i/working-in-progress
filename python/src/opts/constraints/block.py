from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import pulp


class BlockConstraint(ConstraintBase):
    """
    A concrete implementation of the ConstraintBase class for block constraints.
    """

    def __init__(self, id: str = None):
        """
        Initializes a new instance of the Block class.

        Args:
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        super().__init__(ConstraintType.BLOCK, id)

    def apply(self, model: AnualModel):
        """
        Applies the block constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        for h in model.dto.homeroom_list:
            for d in model.dto.day_of_week:
                for p in model.dto.schedule[h][d]:
                    for block in model.dto.curriculum_dict[h]:
                        if len(block) > 1:  # Only blocks with multiple lanes
                            sums_of_x_in_lanes = [pulp.lpSum([model.x[h, d, p, c] for c in lane]) for lane in block]
                            for i in range(1, len(sums_of_x_in_lanes)):
                                model.prob += sums_of_x_in_lanes[0] == sums_of_x_in_lanes[i]
