from opts.constraints.block import BlockConstraint


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
