from common.constants import ConstraintType
from cruds.anual_data_repository import AnulalDataRepository
from opts.anual_model import AnualModel
from utils.solution_extractor import extract_solution


class AnualExcecutor:
    def __init__(self, repository: AnulalDataRepository):
        self.repository = repository

    def solve_schedule(self):
        model = AnualModel()

        constraint_list = self.repository.constraint.find_by_ttid()

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
