from opts.constraints.base import ConstraintBase
from opts.anual_model import AnualModel


class CourseConstraint(ConstraintBase):
    def apply(self, model: AnualModel) -> AnualModel:
        for c in model.dto.C:
            for d in model.dto.D:
                for p in range(1, 8):  # For each period
                    related_classes = [
                        h for h in model.dto.H
                        if (h, d, p, c) in model.x  # Only consider classes with defined variables
                    ]

                    if len(related_classes) > 1:
                        first_class = related_classes[0]
                        for h in related_classes[1:]:
                            model.problem += (
                                model.x[first_class, d, p, c] == model.x[h, d, p, c]
                            )
        return model
