from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class CreditConstraint(ConstraintBase):
    def __init__(self, course_credit_dict: dict):
        self.course_credit_dict = course_credit_dict

    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.data.H:
            for block in model.data.curriculum_dict[h]:
                for lane in block:
                    for c in lane:
                        credit = self.course_credit_dict.get(c, 0)  # Get credit value, default to 0 if not found
                        model.problem += pulp.lpSum(
                            [model.x[h, d, p, c] for d in model.data.D for p in model.data.periods[h][d]]
                        ) == credit
        return model
