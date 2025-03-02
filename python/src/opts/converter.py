from models.homeroom import HomeroomSchema
from src.models.schedule import ScheduleSchema


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
