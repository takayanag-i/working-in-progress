import pytest
from models.constraint import ConstraintSchema
from opts.anual_executor import get_constraints
from opts.constraints.block import BlockConstraint


@pytest.fixture
def constraint_schemas():
    """テスト用の ConstraintSchema リストを作成"""
    return [
        ConstraintSchema(
            id="",
            doc_type="",
            ttid="",
            constraint_type="block",
            parameters={}
        ),
        ConstraintSchema(
            id="",
            doc_type="",
            ttid="",
            constraint_type="invalid",
            parameters={}
        )
    ]


def test_get_constraints(constraint_schemas):
    constraints = get_constraints(constraint_schemas)

    assert len(constraints) == 1
    assert isinstance(constraints[0], BlockConstraint)
