from typing import Dict, List
from models.curriculum import CurriculumSchema
from models.homeroom import HomeroomSchema
from models.schedule import ScheduleSchema


def convert_homeroom_schema_to_schedule_dict(homeroom_schema: HomeroomSchema) -> dict:
    return {
        homeroom.name: {
            slot.day: list(range(1, slot.last_period + 1))
            for slot in homeroom.slots
        }
        for homeroom in homeroom_schema.homerooms
    }


def convert_schedule_schema_to_day_list(schedule: ScheduleSchema) -> list:
    return list(
        dict.fromkeys(
            slot.day for slot in schedule.slots
            if slot.available
        )
    )


def convert_curriculum_schema_to_curriculum_dict(
    schema: CurriculumSchema
) -> Dict[str, List[List[List[str]]]]:
    return {
        curriculum.homeroom: [
            [lane.courses for lane in block.lanes]
            for block in curriculum.blocks
        ]
        for curriculum in schema.curriculums
    }
