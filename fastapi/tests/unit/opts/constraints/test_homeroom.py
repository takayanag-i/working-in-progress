import pulp
from opts.constraints.homeroom import HomeroomConstraint


def test_homeroom_constraint(mock_anual_model):
    homeroom_constraint = HomeroomConstraint()
    model = homeroom_constraint.apply(mock_anual_model)

    expected_constraints = [
        {
            "sense": pulp.LpConstraintEQ,
            "coefficients": [
                {"name": "x_H1_mon_1_C1", "value": 1},
                {"name": "x_H1_mon_2_C1", "value": 1},
                {"name": "x_H1_tue_1_C1", "value": 1},
                {"name": "x_H1_tue_2_C1", "value": 1},
            ],
            "constant": -3,
        },
    ]

    actual_constraints = [v.toDict() for v in model.problem.constraints.values()]

    assert len(actual_constraints) == 6, "数が合わない"

    for expected, acutual in zip(expected_constraints, actual_constraints):
        assert expected["sense"] == acutual["sense"]
        assert expected["constant"] == acutual["constant"]

        expected_coefficients = expected["coefficients"]
        acutual_coefficients = acutual["coefficients"]

        assert len(expected_coefficients) == len(acutual_coefficients)

        for e, a in zip(expected_coefficients, acutual_coefficients):
            assert e["name"] == a["name"]
            assert e["value"] == a["value"]
