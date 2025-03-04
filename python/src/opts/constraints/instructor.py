from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel


class TeacherConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        for d in model.dto.D:
            for p in range(1, 8):
                for t in model.dto.I:
                    model.problem += model.y[d, p, t] <= 1
        return model
