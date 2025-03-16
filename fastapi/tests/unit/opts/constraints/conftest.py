import pytest

from opts.anual_model import AnualData, AnualModel


@pytest.fixture
def mock_anual_data():
    return AnualData(
        H=["H1", "H2", "H3"],
        D=["mon", "tue"],
        C=["C1", "C2", "C3"],
        I=["I1", "I2"],
        periods={
            "H1": {"mon": [1, 2], "tue": [1, 2]},
            "H2": {"mon": [1, 2, 3], "tue": [1, 2]},
            "H3": {"mon": [1], "tue": [1]}
        },
        max_periods=3,
        curriculums={
            "H1": [[["C1"], ["C2", "C3"]]],  # TODO: test_blockのためのレーン数が足りない
            "H2": [[["C1", "C2"]]],
            "H3": [[["C1"]]]
        },
        course_details={
            "C1": {
                "instructors": ["I1"],
                "credits": 3
            },
            "C2": {
                "instructors": ["I1", "I2"],
                "credits": 2
            },
            "C3": {
                "instructors": ["I2"],
                "credits": 3
            },
        }
    )


@pytest.fixture
def mock_anual_model(mock_anual_data):
    return AnualModel(mock_anual_data)
