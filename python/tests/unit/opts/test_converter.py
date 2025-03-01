import pytest
from opts.converter import convert_homeroom_schema_to_schedule_dict
from models.homeroom import HomeroomSchema, Homeroom, Slot


@pytest.fixture
def sample_homeroom_schema():

    homerooms = [
        Homeroom(name="2-4", slots=[Slot(day="mon", last_period=6), Slot(day="tue", last_period=7)]),
        Homeroom(name="2-5", slots=[Slot(day="wed", last_period=5)])
    ]
    return HomeroomSchema(
        id="",
        doc_type="",
        ttid="",
        homerooms=homerooms
    )


def test_convert_homeroom_schema_to_schedule_dict(sample_homeroom_schema):
    expected_result = {
        "2-4": {
            "mon": [1, 2, 3, 4, 5, 6],
            "tue": [1, 2, 3, 4, 5, 6, 7]
        },
        "2-5": {
            "wed": [1, 2, 3, 4, 5]
        }
    }

    result = convert_homeroom_schema_to_schedule_dict(sample_homeroom_schema)
    assert result == expected_result
