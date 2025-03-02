from functools import reduce
from cruds.constraint.interface import ConstraintRepository
from opts.anual_model import AnualModel
from opts.constraints.base import ConstraintBase
from opts.solution_extractor import extract_solution
from opts.constraints.mapping import CONSTRAINTS
from pulp import LpStatusOptimal
from typing import List, Tuple


class AnualExecutor:
    def __init__(self, repository: ConstraintRepository):
        self.repository = repository

    def get_constraints(self) -> List[ConstraintBase]:
        constraint_schemas = self.repository.find_by_ttid()
        return [
            constraint_type(**schema.parameters) for schema in constraint_schemas
            if (constraint_type := CONSTRAINTS.get(schema.constraint_type.upper()))
        ]

    def apply_all(self, model: AnualModel, constraints: List[ConstraintBase]) -> AnualModel:
        def apply_constraints(model: AnualModel, constraint: ConstraintBase) -> AnualModel:
            return constraint.apply(model)

        return reduce(apply_constraints, constraints, model)

    def solve(self, model: AnualModel) -> Tuple[AnualModel, int]:
        status = model.prob.solve()
        return model, status

    def execute(self, model: AnualModel) -> dict:
        constraints = self.get_constraints()
        model = self.apply_all(model, constraints)

        model, status = self.solve(model)

        if status != LpStatusOptimal:
            return {"status": "error", "message": f"Solver failed with status {status}"}

        return extract_solution(model)
