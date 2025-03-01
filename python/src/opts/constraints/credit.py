from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import pulp


class CreditConstraint(ConstraintBase):
    """
    A concrete implementation of the ConstraintBase class for course credit constraints.
    """

    def __init__(self, course_credit_dict: dict, id: str = None):
        """
        Initializes a new instance of the Credit class.

        Args:
            course_credit_dict (dict): Dictionary mapping course IDs to their credit values.
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        super().__init__(ConstraintType.CREDIT, id)
        self.course_credit_dict = course_credit_dict

    def apply(self, model: AnualModel):
        """
        Applies the course credit constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        for h in model.dto.homeroom_list:
            for block in model.dto.curriculum_dict[h]:
                for lane in block:
                    for c in lane:
                        credit = self.course_credit_dict.get(c, 0)  # Get credit value, default to 0 if not found
                        model.prob += pulp.lpSum(
                            [model.x[h, d, p, c] for d in model.dto.day_of_week for p in model.dto.schedule[h][d]]
                        ) == credit
