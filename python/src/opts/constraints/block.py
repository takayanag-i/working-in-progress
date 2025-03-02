from constraints.base import ConstraintBase
from common.constants import ConstraintType
from opts.anual_model import AnualModel
import pulp


class BlockConstraint(ConstraintBase):

    def __init__(self, id: str = None):
        super().__init__(ConstraintType.BLOCK, id)

    def apply(self, model: AnualModel):
        for h in model.dto.homeroom_list:
            for d in model.dto.day_of_week:
                for p in model.dto.schedule[h][d]:
                    for block in model.dto.curriculum_dict[h]:
                        if len(block) > 1:  # Only blocks with multiple lanes
                            sums_of_x_in_lanes = [pulp.lpSum([model.x[h, d, p, c] for c in lane]) for lane in block]
                            for i in range(1, len(sums_of_x_in_lanes)):
                                model.prob += sums_of_x_in_lanes[0] == sums_of_x_in_lanes[i]

        return model
