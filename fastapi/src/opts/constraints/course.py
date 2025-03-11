from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel


class CourseConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        constraints = [
            model.x[enrolled_homerooms[0], d, p, c] == model.x[enrolled_homeroom, d, p, c]
            for c in model.data.C
            for d in model.data.D
            for p in range(1, 8)
            if (
                #  d, pにcを受講しているhのリスト
                enrolled_homerooms := [
                    h for h in model.data.H if (h, d, p, c) in model.x
                ]
            ) and len(enrolled_homerooms) > 1
            for enrolled_homeroom in enrolled_homerooms[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
