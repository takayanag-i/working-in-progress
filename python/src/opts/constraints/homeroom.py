from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class HomeroomConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.dto.homeroom_list:
            for d in model.dto.day_of_week:
                for p in model.dto.schedule[h][d]:
                    model.prob += pulp.lpSum(
                        [model.x[h, d, p, c] for block in model.dto.curriculum_dict[h] for lane in block for c in lane]
                    ) >= 1
        return model
