from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel
import pulp


class BlockConstraint(ConstraintBase):
    def apply(self, model: AnualModel):
        for h in model.dto.H:
            for d in model.dto.D:
                for p in model.dto.periods[h][d]:
                    for block in model.dto.curriculum_dict[h]:
                        if len(block) > 1:  # Only blocks with multiple lanes
                            sums_of_x_in_lanes = [pulp.lpSum([model.x[h, d, p, c] for c in lane]) for lane in block]
                            for i in range(1, len(sums_of_x_in_lanes)):
                                model.problem += sums_of_x_in_lanes[0] == sums_of_x_in_lanes[i]

        return model
