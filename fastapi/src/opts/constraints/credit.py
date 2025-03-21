from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class CreditConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        constraints = [
            pulp.lpSum(
                [model.x[h, d, p, c] for d in model.data.D for p in model.data.periods[h][d]]
            ) == model.data.course_details[c].credits
            for h in model.data.H
            for block in model.data.curriculums[h]
            for lane in block
            for c in lane
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
