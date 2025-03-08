import pytest
import pulp
from opts.anual_model import AnualData, AnualModel  # 実際のモジュール名に置き換えてください


@pytest.fixture
def sample_anual_data():
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
            "H1": [[["C1"]], [["C2"]]],
            "H2": [[["C1", "C2"]]]
        },
        course_details={
            "C1": ["I1"],
            "C2": ["I1", "I2"]
        }
    )


def test_define_variables_x(sample_anual_data):
    model = AnualModel(sample_anual_data)

    # 期待される x のキーと値の検証（列挙）
    expected_x_keys = [
        ("H1", "mon", 1, "C1"),
        ("H1", "mon", 1, "C2"),
        ("H1", "mon", 2, "C1"),
        ("H1", "mon", 2, "C2"),
        ("H1", "tue", 1, "C1"),
        ("H1", "tue", 1, "C2"),
        ("H1", "tue", 2, "C1"),
        ("H1", "tue", 2, "C2"),
        ("H2", "mon", 1, "C1"),
        ("H2", "mon", 1, "C2"),
        ("H2", "mon", 2, "C1"),
        ("H2", "mon", 2, "C2"),
        ("H2", "mon", 3, "C1"),
        ("H2", "mon", 3, "C2"),
        ("H2", "tue", 1, "C1"),
        ("H2", "tue", 1, "C2"),
        ("H2", "tue", 2, "C1"),
        ("H2", "tue", 2, "C2"),
    ]

    assert set(model.x.keys()) == set(expected_x_keys)

    for key in expected_x_keys:
        assert isinstance(model.x[key], pulp.LpVariable)
        assert model.x[key].upBound == 1
        assert model.x[key].lowBound == 0
        assert model.x[key].cat == pulp.LpInteger


def test_define_variables_y(sample_anual_data):
    model = AnualModel(sample_anual_data)

    # 期待される y のキーと値の検証（列挙）
    expected_y_keys = [
        ("mon", 1, "I1"),
        ("mon", 1, "I2"),
        ("mon", 2, "I1"),
        ("mon", 2, "I2"),
        ("mon", 3, "I1"),
        ("mon", 3, "I2"),
        ("tue", 1, "I1"),
        ("tue", 1, "I2"),
        ("tue", 2, "I1"),
        ("tue", 2, "I2"),
        ("tue", 3, "I1"),
        ("tue", 3, "I2"),
    ]

    assert set(model.y.keys()) == set(expected_y_keys)

    for key in expected_y_keys:
        assert isinstance(model.y[key], pulp.LpAffineExpression)
