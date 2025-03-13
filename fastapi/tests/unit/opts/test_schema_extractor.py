import pytest
from models.course import CourseSchema, Course, CourseDetail
from models.curriculum import Block, Curriculum, CurriculumSchema, Lane
from models.homeroom import HomeroomSchema, Homeroom, Slot as HomeroomSlot
from models.instructor import Instructor, InstructorSchema, Slot as InstructorSlot
from models.schedule import ScheduleSchema, Day as ScheduleSlot
from opts.anual_data import CourseDetail as AnualCourseDetail
from opts.schema_extractor import get_course_list, get_max_periods
from opts.schema_extractor import get_curriculums
from opts.schema_extractor import get_periods
from opts.schema_extractor import get_day_list
from opts.schema_extractor import get_course_details
from opts.schema_extractor import get_instructor_list


@pytest.fixture
def sample_course_schema():
    return CourseSchema(
        id="",
        doc_type="",
        ttid="",
        courses=[
            Course(
                name="math",
                subject="math",
                credits=1,
                details=[
                    CourseDetail(instructor="instructor1", room="room1"),
                    CourseDetail(instructor="instructor2", room="room2")
                ]
            ),
            Course(
                name="science",
                subject="science",
                credits=2,
                details=[
                    CourseDetail(instructor="instructor3", room="room3"),
                    CourseDetail(instructor="instructor4", room="room4")
                ]
            )
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


@pytest.fixture
def sample_homeroom_schema():
    return HomeroomSchema(
        id="",
        doc_type="",
        ttid="",
        homerooms=[
            Homeroom(name="2-4",
                     slots=[
                         HomeroomSlot(day="mon", last_period=6),
                         HomeroomSlot(day="tue", last_period=7)
                     ]),
            Homeroom(name="2-5", slots=[HomeroomSlot(day="wed", last_period=5)])
        ]
    )


@pytest.fixture
def sample_instructor_schema():
    return InstructorSchema(
        id="",
        doc_type="",
        ttid="",
        instructors=[
            Instructor(
                name="instructor1",
                discipline="math",
                credits=16,
                slots=[
                    InstructorSlot(day="mon", period=1, available=True),
                    InstructorSlot(day="wed", period=2, available=True)
                ]
            ),
            Instructor(
                name="instructor2",
                discipline="science",
                credits=16,
                slots=[InstructorSlot(day="tue", period=2, available=True)]
            ),
            Instructor(
                name="instructor3",
                discipline="history",
                credits=16,
                slots=[InstructorSlot(day="wed", period=3, available=True)]
            ),
            Instructor(
                name="instructor4",
                discipline="english",
                credits=16,
                slots=[InstructorSlot(day="thu", period=4, available=True)]
            )
        ]
    )


@pytest.fixture
def sample_schedule_schema():
    return ScheduleSchema(
        id="",
        doc_type="",
        ttid="",
        days=[
            ScheduleSlot(name="mon", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(name="tue", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(name="wed", available=True, am_periods=4, pm_periods=3),
            ScheduleSlot(name="sat", available=False)
        ],
        maxPeriods=3,
    )


def test_get_day_list(sample_schedule_schema):
    result1 = get_day_list(sample_schedule_schema)
    assert result1 == ["mon", "tue", "wed"]


def test_get_max_periods(sample_schedule_schema):
    result = get_max_periods(sample_schedule_schema)
    assert result == 3


def test_get_course_list(sample_course_schema):
    result = get_course_list(sample_course_schema)
    assert result == ['math', 'science']


def test_get_instructor_list(sample_instructor_schema):
    result = get_instructor_list(sample_instructor_schema)
    assert result == ["instructor1", "instructor2", "instructor3", "instructor4"]


def test_get_periods(sample_homeroom_schema):

    result = get_periods(sample_homeroom_schema)
    assert result == {
        "2-4": {
            "mon": [1, 2, 3, 4, 5, 6],
            "tue": [1, 2, 3, 4, 5, 6, 7]
        },
        "2-5": {
            "wed": [1, 2, 3, 4, 5]
        }
    }


def test_get_curriculums(sample_curriculum_schema):
    result = get_curriculums(sample_curriculum_schema)
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


def test_get_course_details(sample_course_schema):
    result = get_course_details(sample_course_schema)
    assert result == {
        'math': AnualCourseDetail(
            instructors=['instructor1', 'instructor2'],
            credits=1),
        'science': AnualCourseDetail(
            instructors=['instructor3', 'instructor4'],
            credits=2)
    }
