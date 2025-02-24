from cruds.constraint.interface import ConstraintRepository
from common.constants import ConstraintType
from opts.anual_model import AnualModel
from utils.solution_extractor import extract_solution


class AnualExcecutor:
    def __init__(self, constraint_repository: ConstraintRepository):
        self.constraint_repository = constraint_repository

    def solve_schedule(self):
        constraint_list = self.constraint_repository.find_by_ttid()
        model = AnualModel()

        for constraint_data in constraint_list:
            constraint_type_str = constraint_data["constraint_type"]

            try:
                constraint_type = ConstraintType[constraint_type_str.upper()]
                constraint = constraint_type(
                    id=constraint_data["id"],
                    **constraint_data["parameters"]
                )
                constraint.apply(model)

            except KeyError:
                return {"status": "error", "message": f"Unknown constraint type: {constraint_type_str}"}
            except Exception as e:
                return {"status": "error", "message": f"Invalid constraint data: {str(e)}"}

        model.prob.solve()

        return extract_solution(model)
