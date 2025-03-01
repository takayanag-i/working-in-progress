from models.homeroom import HomeroomSchema


def convert_homeroom_schema_to_schedule_dict(homeroom_schema: HomeroomSchema) -> dict:
    result = {}

    for homeroom in homeroom_schema.homerooms:
        name = homeroom.name
        slots = homeroom.slots

        slots_dict = {
            slot.day: list(range(1, slot.last_period + 1)) for slot in slots
        }

        result[name] = slots_dict

    return result
