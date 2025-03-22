from exceptions.opts import OptimizationError
from models.constraint import ConstraintSchema
from opts.anual_model import AnualModel
from opts.constraints.base import ConstraintBase
from opts.constraints.mapping import CONSTRAINT_TYPES_BUILT_IN, CONSTRAINT_TYPES_MANDATORY
from pulp import LpStatusOptimal
from typing import List, Tuple


def get_mandatory_constraints():
    return [constraint_cls() for constraint_cls in CONSTRAINT_TYPES_MANDATORY.values()]


def get_built_in_constraints(schemas: List[ConstraintSchema]) -> List[ConstraintBase]:
    return [
        CONSTRAINT_TYPES_BUILT_IN[schema.constraint_type.upper()](**schema.parameters)
        for schema in schemas
    ]  # todo: key error handling


def apply_constraints(model: AnualModel, constraints: List[ConstraintBase]) -> AnualModel:
    for constraint in constraints:
        model = constraint.apply(model)
    return model


def solve(model: AnualModel) -> Tuple[AnualModel, int]:
    status = model.problem.solve()
    return model, status


def execute(model: AnualModel, constraint_schemas: List[ConstraintSchema]):
    constraints = get_mandatory_constraints()

    constraints += get_built_in_constraints(constraint_schemas)

    model = apply_constraints(model, constraints)

    model, status = solve(model)

    if status != LpStatusOptimal:
        raise OptimizationError(status)

    return model
