from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class HomeroomConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        constraints = [
            pulp.lpSum(
                [model.x[h, d, p, c] for block in model.data.curriculums[h] for lane in block for c in lane]
            ) >= 1
            for h in model.data.H
            for d in model.data.D
            for p in model.data.periods[h][d]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
