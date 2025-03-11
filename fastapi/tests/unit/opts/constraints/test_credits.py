from opts.constraints.credit import CreditConstraint


def test_credit_constraint(mock_anual_model):
    credit_constraint = CreditConstraint()
    model = credit_constraint.apply(mock_anual_model)

    actual_constraints = [
        (d["name"], d["value"], v.toDict()["constant"])
        for v in model.problem.constraints.values()
        for d in v.toDict()["coefficients"]
    ]

    assert len(actual_constraints) == 24, "数が合わない"
