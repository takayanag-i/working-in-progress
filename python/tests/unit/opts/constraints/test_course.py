from opts.constraints.course import CourseConstraint


def test_course_constraint(mock_anual_model):
    course_constraint = CourseConstraint()
    model = course_constraint.apply(mock_anual_model)

    expected_constraints = [
        # C1 の制約
        {("x_H1_mon_1_C1", 1), ("x_H2_mon_1_C1", -1)},
        {("x_H1_mon_2_C1", 1), ("x_H2_mon_2_C1", -1)},
        {("x_H1_tue_1_C1", 1), ("x_H2_tue_1_C1", -1)},
        {("x_H1_tue_2_C1", 1), ("x_H2_tue_2_C1", -1)},
        {("x_H1_mon_1_C1", 1), ("x_H3_mon_1_C1", -1)},
        {("x_H1_tue_1_C1", 1), ("x_H3_tue_1_C1", -1)},

        # C2 の制約
        {("x_H1_mon_1_C2", 1), ("x_H2_mon_1_C2", -1)},
        {("x_H1_mon_2_C2", 1), ("x_H2_mon_2_C2", -1)},
        {("x_H1_tue_1_C2", 1), ("x_H2_tue_1_C2", -1)},
        {("x_H1_tue_2_C2", 1), ("x_H2_tue_2_C2", -1)},
    ]

    actual_constraints = [
        {
            (d["name"], d["value"])
            for d in constraint.toDict()["coefficients"]
        }
        for constraint in model.problem.constraints.values()
    ]

    assert len(actual_constraints) == 10, "数が合わない"

    for expected in expected_constraints:
        assert expected in actual_constraints, f"期待する制約が見つからない: {expected}"
