import pytest
from models.curriculum import Block, Curriculum, CurriculumSchema, Lane
from opts.converter import convert_curriculum_schema_to_curriculum_dict, convert_homeroom_schema_to_schedule_dict
from models.homeroom import HomeroomSchema, Homeroom, Slot

from src.opts.converter import convert_schedule_schema_to_day_list
from src.models.schedule import ScheduleSchema, Slot as ScheduleSlot


@pytest.fixture
def sample_homeroom_schema():
    return HomeroomSchema(
        id="",
        doc_type="",
        ttid="",
        homerooms=[
            Homeroom(name="2-4", slots=[Slot(day="mon", last_period=6), Slot(day="tue", last_period=7)]),
            Homeroom(name="2-5", slots=[Slot(day="wed", last_period=5)])
        ]
    )


@pytest.fixture
def sample_schedule_schema():
    return ScheduleSchema(
        id="",
        doc_type="",
        ttid="",
        slots=[
            ScheduleSlot(day="mon", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(day="tue", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(day="wed", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(day="sat", available=False)
        ]
    )


@pytest.fixture
def sample_curriculum_schema():
    return CurriculumSchema(
        id="",
        doc_type="",
        ttid="",
        curriculums=[
            Curriculum(
                homeroom="2-4",
                blocks=[
                    Block(
                        name="block1",
                        lanes=[
                            Lane(courses=["math", "science"]),
                            Lane(courses=["history", "english"])
                        ]
                    ),
                    Block(
                        name="block2",
                        lanes=[
                            Lane(courses=["math", "science"]),
                            Lane(courses=["history", "english"])
                        ]
                    )
                ]
            ),
            Curriculum(
                homeroom="2-5",
                blocks=[
                    Block(
                        name="block1",
                        lanes=[
                            Lane(courses=["math", "science"]),
                            Lane(courses=["history", "english"])
                        ]
                    ),
                    Block(
                        name="block2",
                        lanes=[
                            Lane(courses=["math", "science"]),
                            Lane(courses=["history", "english"])
                        ]
                    )
                ]
            )
        ]
    )


def test_convert_homeroom_schema_to_schedule_dict(sample_homeroom_schema):

    result = convert_homeroom_schema_to_schedule_dict(sample_homeroom_schema)
    assert result == {
        "2-4": {
            "mon": [1, 2, 3, 4, 5, 6],
            "tue": [1, 2, 3, 4, 5, 6, 7]
        },
        "2-5": {
            "wed": [1, 2, 3, 4, 5]
        }
    }


def test_convert_schedule_schema_to_day_list(sample_schedule_schema):
    result = convert_schedule_schema_to_day_list(sample_schedule_schema)
    assert result == ["mon", "tue", "wed"]


def test_convert_curriculum_schema_to_curriculum_dict(sample_curriculum_schema):
    result = convert_curriculum_schema_to_curriculum_dict(sample_curriculum_schema)
    assert result == {
        "2-4": [
            [["math", "science"], ["history", "english"]],
            [["math", "science"], ["history", "english"]]
        ],
        "2-5": [
            [["math", "science"], ["history", "english"]],
            [["math", "science"], ["history", "english"]]
        ]
    }
