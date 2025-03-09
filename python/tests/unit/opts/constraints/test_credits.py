from opts.constraints.credit import CreditConstraint


def test_credit_constraint(mock_anual_model):
    credit_constraint = CreditConstraint()
    model = credit_constraint.apply(mock_anual_model)

    actual_constraints = [
        constraint.toDict() for constraint in model.problem.constraints.values()
    ]

    pass
