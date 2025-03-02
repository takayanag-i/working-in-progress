from functools import reduce
from models.constraint import ConstraintSchema
from opts.anual_model import AnualModel
from opts.constraints.base import ConstraintBase
from opts.solution_extractor import extract_solution
from opts.constraints.mapping import CONSTRAINT_TYPES
from pulp import LpStatusOptimal
from typing import List, Tuple


def get_constraints(schemas: List[ConstraintSchema]) -> List[ConstraintBase]:
    return [
        type(**schema.parameters) for schema in schemas
        if (type := CONSTRAINT_TYPES.get(schema.constraint_type.upper()))
    ]


def apply_all(model: AnualModel, constraints: List[ConstraintBase]) -> AnualModel:
    def apply_constraints(model: AnualModel, constraint: ConstraintBase) -> AnualModel:
        return constraint.apply(model)

    return reduce(apply_constraints, constraints, model)


def solve(model: AnualModel) -> Tuple[AnualModel, int]:
    status = model.prob.solve()
    return model, status


def execute(model: AnualModel, constraint_schemas: List[ConstraintSchema]) -> dict:
    constraints = get_constraints(constraint_schemas)
    model = apply_all(model, constraints)

    model, status = solve(model)

    if status != LpStatusOptimal:
        return {"status": "error", "message": f"Solver failed with status {status}"}

    return extract_solution(model)
