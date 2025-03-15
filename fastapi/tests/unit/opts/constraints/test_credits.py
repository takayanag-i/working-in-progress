import pulp
from opts.constraints.credit import CreditConstraint


def test_credit_constraint(mock_anual_model):
    credit_constraint = CreditConstraint()
    model = credit_constraint.apply(mock_anual_model)

    expected_constraints = [
        {
            "sence": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_1_C2", "value": -1},
                {"name": "x_H1_mon_1_C3", "value": -1},
            ],
            "constant": 1,
        },
        {
            "sence": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_mon_2_C2", "value": -1},
                {"name": "x_H1_mon_2_C3", "value": -1},
            ],
            "constant": 1,
        },
        {
            "sence": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_1_C2", "value": -1},
                {"name": "x_H1_tue_1_C3", "value": -1},
            ],
            "constant": 1,
        },
        {
            "sence": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_tue_2_C1", "value": 1},
                {"name": "x_H1_tue_2_C2", "value": -1},
                {"name": "x_H1_tue_2_C3", "value": -1},
            ],
            "constant": 1,
        },
    ]

    # actual_constraints = [
    #     (d["name"], d["value"], v.toDict()["constant"])
    #     for v in model.problem.constraints.values()
    #     for d in v.toDict()["coefficients"]
    # ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 24, "数が合わない"
    for e, a in zip(expected_constraints, actual_constraints):
        assert e["sence"] == a["sence"], "senceが合わない"
