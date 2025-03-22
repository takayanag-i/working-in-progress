from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel


class CourseConstraint(ConstraintBase):
    """講座制約

    - (システム表現)任意の曜日・時限で、任意の講座に対して、開講バイナリの値はその講座を受講する学級どうしで互いに等しい。
    """

    def apply(self, model: AnualModel) -> AnualModel:
        constraints = [
            model.x[enrolled_homerooms[0], d, p, c] == model.x[enrolled_homeroom, d, p, c]
            for c in model.data.C
            for d in model.data.D
            for p in model.data.P
            if (
                #  cを受講しているhのリスト
                enrolled_homerooms := [
                    h for h in model.data.H
                    if (h, d, p, c) in model.x  # cがあるかと、d, pがあるかのチェック
                ]
            ) and len(enrolled_homerooms) > 1
            for enrolled_homeroom in enrolled_homerooms[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
