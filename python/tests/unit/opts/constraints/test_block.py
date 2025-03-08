import pytest
from opts.anual_model import AnualData, AnualModel
from opts.constraints.block import BlockConstraint


@pytest.fixture
def mock_anual_data():
    return AnualData(
        H=["H1", "H2"],
        D=["mon", "tue"],
        C=["C1", "C2"],
        I=["I1", "I2"],
        periods={
            "H1": {"mon": [1, 2], "tue": [1, 2]},
            "H2": {"mon": [1, 2, 3], "tue": [1, 2]}
        },
        curriculums={
            "H1": [[["C1"], ["C2", "C3"]]],
            "H2": [[["C1", "C2"]]]
        },
        course_details={
            "C1": ["I1"],
            "C2": ["I1", "I2"]
        }
    )


@pytest.fixture
def mock_anual_model(mock_anual_data):
    return AnualModel(mock_anual_data)


def test_block_constraint(mock_anual_model):
    constraint = BlockConstraint()

    expected_constraints = [
        {("x_H1_mon_1_C1", 1), ("x_H1_mon_1_C2", -1), ("x_H1_mon_1_C3", -1)},
        {("x_H1_mon_2_C1", 1), ("x_H1_mon_2_C2", -1), ("x_H1_mon_2_C3", -1)},
        {("x_H1_tue_1_C1", 1), ("x_H1_tue_1_C2", -1), ("x_H1_tue_1_C3", -1)},
        {("x_H1_tue_2_C1", 1), ("x_H1_tue_2_C2", -1), ("x_H1_tue_2_C3", -1)},
    ]

    model = constraint.apply(mock_anual_model)

    actual_constraints = [
        {
            (d["name"], d["value"])
            for d in constraint.toDict()["coefficients"]
        }
        for constraint in model.problem.constraints.values()
    ]
    assert len(actual_constraints) == 4, f"制約数が想定と異なる: {len(actual_constraints)} 個"

    for expected in expected_constraints:
        assert expected in actual_constraints, f"期待する制約が見つからない: {expected}"
