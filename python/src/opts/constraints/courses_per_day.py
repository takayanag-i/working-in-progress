from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class CoursesPerDayConstraint(ConstraintBase):
    def __init__(self, twice_course_list: list):
        self.twice_course_list = twice_course_list

    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.dto.homeroom_list:
            for c in model.dto.course_list:
                max = 2 if c in self.twice_course_list else 1
                for d in model.dto.day_of_week:
                    valid_x = [
                        model.x[h, d, p, c] for p in model.dto.schedule[h][d] if (h, d, p, c) in model.x
                    ]
                    if valid_x:
                        model.prob += pulp.lpSum(valid_x) <= max
        return model
