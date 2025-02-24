from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel


class CourseConstraint(ConstraintBase):
    """
    A concrete implementation of the ConstraintBase class for course constraints.
    """

    def __init__(self, id: str = None):
        """
        Initializes a new instance of the Course class.

        Args:
            id (str, optional): Unique identifier for the constraint. If not provided, a new UUID will be generated.
        """
        super().__init__(ConstraintType.COURSE, id)

    def apply(self, model: AnualModel):
        """
        Applies the course constraint to the given model.

        Args:
            model (AnualSolver): The model to which the constraint will be applied.
        """
        for c in model.dto.course_list:
            for d in model.dto.day_of_week:
                for p in range(1, 8):  # For each period
                    related_classes = [
                        h for h in model.dto.homeroom_list
                        if (h, d, p, c) in model.x  # Only consider classes with defined variables
                    ]

                    if len(related_classes) > 1:
                        first_class = related_classes[0]
                        for h in related_classes[1:]:
                            model.prob += (
                                model.x[first_class, d, p, c] == model.x[h, d, p, c]
                            )
