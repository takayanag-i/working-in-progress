from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class BlockConstraint(ConstraintBase):
    """ブロック制約

    - 任意の学級の任意の曜日・時限で、任意のブロックに対して、ブロックの各レーンに含まれる講座の開講バイナリの総和はレーンどうしで互いに等しい。
    - ブロックに含まれるレーンが1つだけの場合は、制約条件式を生成しない。
    """

    def apply(self, model: AnualModel):
        constraints = [
            lane_sums[0] == lane_sum
            for h in model.data.H
            for d in model.data.D
            for p in model.data.periods[h][d]
            for block in model.data.curriculums[h]
            if len(block) > 1
            and (
                lane_sums := [
                    pulp.lpSum([model.x[h, d, p, c] for c in lane])
                    for lane in block
                ]
            )
            for lane_sum in lane_sums[1:]
        ]

        for constraint in constraints:
            model.problem += constraint

        return model
