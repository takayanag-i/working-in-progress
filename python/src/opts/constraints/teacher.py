from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel


class TeacherConstraint(ConstraintBase):
    def __init__(self):
        super().__init__(ConstraintType.TEACHER, id)

    def apply(self, model: AnualModel) -> AnualModel:
        for d in model.dto.day_of_week:
            for p in range(1, 8):
                for t in model.dto.teacher_list:
                    model.prob += model.y[d, p, t] <= 1
        return model
