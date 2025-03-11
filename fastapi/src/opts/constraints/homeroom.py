from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class HomeroomConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.data.H:
            for d in model.data.D:
                for p in model.data.periods[h][d]:
                    model.problem += pulp.lpSum(
                        [model.x[h, d, p, c] for block in model.data.curriculum_dict[h] for lane in block for c in lane]
                    ) >= 1
        return model
