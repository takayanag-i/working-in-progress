from typing import Dict, List
from models.course import CourseSchema
from models.curriculum import CurriculumSchema
from models.homeroom import HomeroomSchema
from models.instructor import InstructorSchema
from models.schedule import ScheduleSchema
from opts.anual_data import CourseDetail


def get_day_list(schedule: ScheduleSchema) -> List[str]:
    """ScheduleSchemaから曜日のリストを取得する。

    Args:
        schedule (ScheduleSchema)

    Returns:
        List[str]: 曜日リスト
    """
    return list(
        dict.fromkeys(
            day.day for day in schedule.days
            if day.available
        )
    )


def get_period_list(schedule: ScheduleSchema) -> List[int]:
    """
    ScheduleSchemaからの時限リストを取得する。

    Args:
        schedule (ScheduleSchema)

    Returns:
        List[int]: 時限リスト
    """
    return list(range(
        1,
        max(
            (day.am_periods + day.pm_periods)
            for day in schedule.days
            if day.available
        ) + 1
    ))


def get_instructor_list(schema: InstructorSchema) -> List[str]:
    """
    InstructorSchemaから教員名リストを取得する。

    Args:
        schema (InstructorSchema)

    Returns:
        List[str]: 教員名リスト
    """
    return list(
        dict.fromkeys(
            instructor.name for instructor in schema.instructors
        )
    )


def get_course_list(schema: CourseSchema) -> List[str]:
    """
    CourseSchemaから講座名リストを取得する。

    Args:
        schema (CourseSchema)

    Returns:
        List[str]: 講座名リスト
    """

    return list(
        dict.fromkeys(
            course.name for course in schema.courses
        )
    )


def get_homeroom_list(schema: HomeroomSchema) -> List[str]:
    """
    HomeroomSchemaから学級リストを取得する。

    Args:
        schema (HomeroomSchema)

    Returns:
        List[str]: 学級リスト
    """
    return list(
        dict.fromkeys(
            homeroom.homeroom for homeroom in schema.homerooms
        )
    )


def get_periods(homeroom_schema: HomeroomSchema) -> Dict[str, Dict[str, List[int]]]:
    """
    HomeroomSchemaから{学級:時限リスト}辞書を取得する。

    Args:
        homeroom_schema (HomeroomSchema)

    Returns:
        Dict[str, Dict[str, List[int]]]: 学級をキーとし、各曜日の利用可能な時限リストを格納した辞書。
        例:
        {
            "2-4": {
                "mon": [1, 2, 3, 4, 5],
                "tue": [1, 2, 3, 4, 5, 6]
            },
            "2-5": {
                "mon": [1, 2, 3, 4],
                "tue": [1, 2, 3, 4, 5]
            }
        }
    """

    return {
        homeroom.homeroom: {
            day.day: list(range(1, day.last_period + 1))
            for day in homeroom.days
        }
        for homeroom in homeroom_schema.homerooms
    }


def get_curriculums(schema: CurriculumSchema) -> Dict[str, List[List[List[str]]]]:
    """
    CurriculumSchemaから各学級のカリキュラムを取得する。

    Args:
        schema (CurriculumSchema)

    Returns:
        Dict[str, List[List[List[str]]]]: 学級ごとのカリキュラム。
        例:
        {
            "2-4": [
                [["数学", "英語"], ["理科", "社会"]],
                [["音楽"], ["体育"]]
            ],
            "2-5": [
                [["国語", "数学"], ["美術"]],
                [["英語", "理科"]]
            ]
        }
    """
    return {
        curriculum.homeroom: [
            [lane.courses for lane in block.lanes]
            for block in curriculum.blocks
        ]
        for curriculum in schema.curriculums
    }


def get_course_details(course_schema: CourseSchema) -> Dict[str, CourseDetail]:
    """
    CourseSchemaからCourseDetail（教員リスト、単位数）を取得する。

    Args:
        course_schema (CourseSchema)

    Returns:
        Dict[str, CourseDetail]: 講座名をキーとし、教員リストと単位数を格納した `CourseDetail` オブジェクトを値とする辞書。
        例:
        {
            "数学II": CourseDetail(instructors=["田中", "鈴木"], credits=2),
            "英語表現": CourseDetail(instructors=["佐藤"], credits=3)
        }
    """
    return {
        course.name: CourseDetail(
            instructors=[detail.instructor for detail in course.details],
            credits=course.credits)
        for course in course_schema.courses
    }
