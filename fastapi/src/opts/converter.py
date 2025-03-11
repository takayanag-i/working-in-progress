from typing import Dict, List
from models.course import CourseSchema
from models.curriculum import CurriculumSchema
from models.homeroom import HomeroomSchema
from models.instructor import InstructorSchema
from models.schedule import ScheduleSchema


def convert_schedule_schema_to_day_list(schedule: ScheduleSchema) -> list:
    """曜日リスト"""
    return list(
        dict.fromkeys(
            slot.day for slot in schedule.slots
            if slot.available
        )
    )


def convert_instructor_schema_to_instructor_list(schema: InstructorSchema) -> list:
    """教員リスト"""
    return list(
        dict.fromkeys(
            instructor.name for instructor in schema.instructors
        )
    )


def convert_course_schema_to_course_list(schema: CourseSchema) -> list:
    """講座リスト"""
    return list(
        dict.fromkeys(
            course.name for course in schema.courses
        )
    )


def convert_homeroom_schema_to_periods(homeroom_schema: HomeroomSchema) -> Dict[str, Dict[str, List[int]]]:
    """{学級: スロット}辞書"""
    return {
        homeroom.name: {
            slot.day: list(range(1, slot.last_period + 1))
            for slot in homeroom.slots
        }
        for homeroom in homeroom_schema.homerooms
    }


def convert_curriculum_schema_to_curriculums(schema: CurriculumSchema) -> Dict[str, List[List[List[str]]]]:
    """{学級: カリキュラム}辞書"""
    return {
        curriculum.homeroom: [
            [lane.courses for lane in block.lanes]
            for block in curriculum.blocks
        ]
        for curriculum in schema.curriculums
    }


def convert_course_schema_to_course_details(course_schema: CourseSchema) -> Dict[str, List[str]]:
    """{講座: 教員リスト}辞書"""
    return {
        course.name:
        {
            "instructors": [detail.instructor for detail in course.details],
            "credits": course.credits
        }
        for course in course_schema.courses
    }
