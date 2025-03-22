import pytest
import pulp
from opts.anual_model import AnualData, AnualModel


@pytest.fixture
def sample_anual_data():
    return AnualData(
        H=["H1", "H2"],
        D=["mon", "tue"],
        P=[1, 2, 3],
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
            "C1": {
                "instructors": ["I1"],
                "credits": 1
            },
            "C2": {
                "instructors": ["I1", "I2"],
                "credits": 1
            },
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


# def test_define_variables_y(sample_anual_data):
