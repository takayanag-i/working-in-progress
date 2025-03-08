from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class CoursesPerDayConstraint(ConstraintBase):
    def __init__(self, twice_course_list: list):
        self.twice_course_list = twice_course_list

    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.data.H:
            for c in model.data.C:
                max = 2 if c in self.twice_course_list else 1
                for d in model.data.D:
                    valid_x = [
                        model.x[h, d, p, c] for p in model.data.periods[h][d] if (h, d, p, c) in model.x
                    ]
                    if valid_x:
                        model.problem += pulp.lpSum(valid_x) <= max
        return model
