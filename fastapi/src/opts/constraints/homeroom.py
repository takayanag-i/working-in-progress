from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class HomeroomConstraint(ConstraintBase):
    """学級制約。

    - (業務表現)学級の空きコマはつくらない。
    - (システム表現)任意の学級の任意の曜日・時限で、その学級のカリキュラムに含まれる講座の開講バイナリの総和は1以上である。
    """

    def apply(self, model: AnualModel) -> AnualModel:
        constraints = [
            pulp.lpSum(
                [model.x[h, d, p, c] for block in model.data.curriculums[h] for lane in block for c in lane]
            ) >= 1
            for h in model.data.H
            for d in model.data.D
            for p in model.data.periods[h][d]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
