from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel


class InstructorConstraint(ConstraintBase):
    """教員制約

    """

    def apply(self, model: AnualModel) -> AnualModel:

        constraints = [
            model.y[d, p, i] <= 1
            for d in model.data.D
            for p in model.data.P
            for i in model.data.I
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
