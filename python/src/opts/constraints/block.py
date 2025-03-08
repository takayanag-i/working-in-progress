from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class BlockConstraint(ConstraintBase):
    def apply(self, model: AnualModel):
        constraints = [
            lane_sums[0] == lane_sum
            for h in model.data.H
            for d in model.data.D
            for p in model.data.periods[h][d]
            for block in model.data.curriculums[h]
            if len(block) > 1
            and (
                lane_sums := [
                    pulp.lpSum([model.x[h, d, p, c] for c in lane])
                    for lane in block
                ]
            )
            for lane_sum in lane_sums[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
