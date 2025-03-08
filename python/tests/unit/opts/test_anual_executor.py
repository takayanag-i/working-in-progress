import pytest
import pulp
from exceptions.opts import ConstraintError, OptimizationError
from models.constraint import ConstraintSchema
from opts.anual_model import AnualModel, AnualData
from opts.constraints.base import ConstraintBase
from opts.constraints.mapping import CONSTRAINT_TYPES
from opts.anual_executor import get_constraints, apply_all, execute


class MockConstraint(ConstraintBase):
    # 学級制約と同一
    def apply(self, model: AnualModel) -> AnualModel:
        for h in model.data.H:
            for d in model.data.D:
                for p in model.data.periods[h][d]:
                    model.problem += pulp.lpSum(
                        [model.x[h, d, p, c] for block in model.data.curriculums[h] for lane in block for c in lane]
                    ) >= 1
        return model


@pytest.fixture(autouse=True)
def setup_mock_constraint():
    CONSTRAINT_TYPES["MOCK"] = MockConstraint


@pytest.fixture
def valid_constraint_schemas():
    return [
        ConstraintSchema(
            id="",
            doc_type="",
            ttid="",
            constraint_type="mock",
            parameters={}
        )
    ]


def invalid_constraint_schemas():
    return [
        ConstraintSchema(
            id="",
            doc_type="",
            ttid="",
            constraint_type="invalid",
            parameters={}
        )
    ]


@pytest.fixture
def sample_anual_data():
    """AnualData のサンプルデータ"""
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


@pytest.fixture
def mock_model(sample_anual_data):
    """AnualModel のモック（model.problem, model.x は AnualModel の実装をそのまま使用）"""
    return AnualModel(sample_anual_data)

##################################################################


def test_get_constraints_success(valid_constraint_schemas):
    constraints = get_constraints(valid_constraint_schemas)
    assert len(constraints) == 1
    assert isinstance(constraints[0], MockConstraint)


def test_apply_all(mock_model):
    constraints = [MockConstraint()]
    mock_model = apply_all(mock_model, constraints)

    # 追加された制約を取得
    constraint_expressions = list(mock_model.problem.constraints.values())

    # 1つ以上の制約が適用されていることを確認
    assert len(constraint_expressions) > 0, "No constraints were added to the model."


def test_execute_success(mock_model, valid_constraint_schemas):
    try:
        execute(mock_model, valid_constraint_schemas)
    except OptimizationError as e:
        pytest.fail(str(e))


def test_execute_no_constraints(mock_model):
    """異常系: execute で制約がない場合 ConstraintError を送出"""
    with pytest.raises(ConstraintError, match="No valid constraints provided"):
        execute(mock_model, [])


def test_execute_optimization_failure(mock_model, valid_constraint_schemas, monkeypatch):
    monkeypatch.setattr(mock_model.problem, "solve", lambda: pulp.LpStatusNotSolved)

    with pytest.raises(OptimizationError):
        execute(mock_model, valid_constraint_schemas)
