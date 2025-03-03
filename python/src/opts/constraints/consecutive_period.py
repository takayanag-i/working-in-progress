from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp
import math


class ConsecutivePeriodConstraint(ConstraintBase):
    def __init__(self, course: str, credit: int):
        self.course = course
        self.credit = credit

    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.dto.H:
            consecutive_list = []
            for d in model.dto.D:
                periods = sorted(model.dto.periods[h][d])
                for i in range(len(periods) - 1):
                    p1, p2 = periods[i], periods[i + 1]
                    if (h, d, p1, self.course) in model.x and (h, d, p2, self.course) in model.x:
                        consecutive = pulp.LpVariable(f"consecutive_{h}_{d}_{p1}_{p2}_{self.course}", cat="Binary")
                        consecutive_list.append(consecutive)
                        model.problem += consecutive <= model.x[h, d, p1, self.course]
                        model.problem += consecutive <= model.x[h, d, p2, self.course]
                        model.problem += model.x[h, d, p1, self.course] + model.x[h, d, p2, self.course] - 1 <= consecutive
                for i in range(len(periods) - 2):
                    p1, p2, p3 = periods[i], periods[i + 1], periods[i + 2]
                    if (h, d, p1, self.course) in model.x and \
                       (h, d, p2, self.course) in model.x and \
                       (h, d, p3, self.course) in model.x:
                        model.problem += model.x[h, d, p1, self.course] + \
                            model.x[h, d, p2, self.course] + \
                            model.x[h, d, p3, self.course] <= 2
            if consecutive_list:
                model.problem += pulp.lpSum(consecutive_list) == math.floor(self.credit / 2)

        return model
