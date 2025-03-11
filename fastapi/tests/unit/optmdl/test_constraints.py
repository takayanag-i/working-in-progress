# import pulp
# import pytest
# from pkgs.optmdl.constraints import *

# @pytest.fixture
# def mock_model(mocker):
#     """Sample fixture to create a mock LpModel for testing."""
#     model = mocker.MagicMock()
#     model.prob = pulp.LpProblem("TestProblem", pulp.LpMinimize)
#     model.dto = mocker.MagicMock()
#     model.dto.homeroom_list = ['H1']
#     model.dto.day_of_week = ['Mon', 'Tue']
#     model.dto.schedule = {'H1': {'Mon': [1, 2], 'Tue': [1, 2]}}
#     model.dto.curriculum_dict = {'H1': [[['C1'], ['C2']]]}
#     model.dto.course_list = ['C1', 'C2']
#     model.dto.teacher_list = ['T1']
#     model.x = {(h, d, p, c): pulp.LpVariable(f"x_{h}_{d}_{p}_{c}", cat='Binary')
#             for h in model.dto.homeroom_list
#             for d in model.dto.day_of_week
#             for p in model.dto.schedule[h][d]
#             for c in model.dto.course_list}
#     return model

# def test_add_homeroom_constraints(mock_model):
#     model = add_homeroom_constraints(mock_model)
#     constraints_dict = model.prob.constraints

#     expected_dict = {
#         "_C1": pulp.LpConstraint(
#             e = pulp.lpSum([mock_model.x['H1', 'Mon', 1, 'C1'], mock_model.x['H1', 'Mon', 1, 'C2']]),
#             sense = pulp.LpConstraintGE,
#             rhs = 1,
#         ),
#         "_C2": pulp.LpConstraint(
#             e = pulp.lpSum([mock_model.x['H1', 'Mon', 2, 'C1'], mock_model.x['H1', 'Mon', 2, 'C2']]),
#             sense = pulp.LpConstraintGE,
#             rhs = 1,
#         ),
#         "_C3": pulp.LpConstraint(
#             e = pulp.lpSum([mock_model.x['H1', 'Tue', 1, 'C1'], mock_model.x['H1', 'Tue', 1, 'C2']]),
#             sense = pulp.LpConstraintGE,
#             rhs = 1,
#         ),
#         "_C4": pulp.LpConstraint(
#             e = pulp.lpSum([mock_model.x['H1', 'Tue', 2, 'C1'], mock_model.x['H1', 'Tue', 2, 'C2']]),
#             sense = pulp.LpConstraintGE,
#             rhs = 1,
#         ),
#     }

#     assert len(constraints_dict) == len(expected_dict), "数が一致しません"
#     for key, expected in expected_dict.items():

#         assert key in expected_dict, f"キーが含まれていません: {key}"
#         actual = constraints_dict[key]

#         assert actual.constant == expected.constant, f"定数が一致しません: {actual.constant} != {expected.constant}"
#         assert actual.sense == expected.sense, f"比較演算子が一致しません: {actual.sense} != {expected.sense}"
#         assert actual.name == expected.name, f"左辺が一致しません: {actual.name} != {expected.name}"
