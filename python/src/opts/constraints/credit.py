from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import pulp


class CreditConstraint(ConstraintBase):
    def __init__(self, course_credit_dict: dict):
        super().__init__(ConstraintType.CREDIT)
        self.course_credit_dict = course_credit_dict

    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.dto.homeroom_list:
            for block in model.dto.curriculum_dict[h]:
                for lane in block:
                    for c in lane:
                        credit = self.course_credit_dict.get(c, 0)  # Get credit value, default to 0 if not found
                        model.prob += pulp.lpSum(
                            [model.x[h, d, p, c] for d in model.dto.day_of_week for p in model.dto.schedule[h][d]]
                        ) == credit
        return model
