from exceptions.opts import ConstraintError, OptimizationError
from models.constraint import ConstraintSchema
from opts.anual_model import AnualModel
from opts.constraints.base import ConstraintBase
from opts.solution_extractor import extract_solution
from opts.constraints.mapping import CONSTRAINT_TYPES
from pulp import LpStatusOptimal
from typing import List, Tuple


def get_constraints(schemas: List[ConstraintSchema]) -> List[ConstraintBase]:
    return [
        CONSTRAINT_TYPES[schema.constraint_type.upper()](**schema.parameters)
        for schema in schemas
    ]  # todo: key error handling


def apply_all(model: AnualModel, constraints: List[ConstraintBase]) -> AnualModel:
    for constraint in constraints:
        model = constraint.apply(model)
    return model


def solve(model: AnualModel) -> Tuple[AnualModel, int]:
    status = model.problem.solve()
    return model, status


def execute(model: AnualModel, constraint_schemas: List[ConstraintSchema]) -> dict:
    constraints = get_constraints(constraint_schemas)
    if not constraints:
        raise ConstraintError("No valid constraints provided")

    model = apply_all(model, constraints)

    model, status = solve(model)

    if status != LpStatusOptimal:
        raise OptimizationError(status)

    return extract_solution(model)
