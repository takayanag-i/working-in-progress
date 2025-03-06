import pytest
import pulp
from opts.anual_model import AnualData, AnualModel  # 実際のモジュール名に置き換えてください


@pytest.fixture
def sample_anual_data():
    return AnualData(
        H=["H1"],
        D=["mon"],
        C=["C1"],
        I=["I1"],
        periods={"H1": {"mon": [1]}},
        curriculums={"H1": [[["C1"]]]},
        course_details={"C1": ["I1"]}
    )


def test_define_variables_x(sample_anual_data):
    model = AnualModel(sample_anual_data)

    # 期待される x のキーと値の検証
    expected_x_keys = [("H1", "mon", 1, "C1")]
    assert set(model.x.keys()) == set(expected_x_keys)
    for key in expected_x_keys:
        assert isinstance(model.x[key], pulp.LpVariable)
        # cat='Binary'の確認
        assert model.x[key].upBound == 1
        assert model.x[key].lowBound == 0
        assert model.x[key].cat == pulp.LpInteger


def test_define_variables_y(sample_anual_data):
    model = AnualModel(sample_anual_data)

    # 期待される y のキーと値の検証
    expected_y_keys = [("mon", 1, "I1")]
    assert set(model.y.keys()) == set(expected_y_keys)
    for key in expected_y_keys:
        assert isinstance(model.y[key], pulp.LpAffineExpression)
        assert len(model.y[key].terms) == 1  # 期待される項数の確認
