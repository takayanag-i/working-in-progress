from models.homeroom import HomeroomSchema


def convert_homeroom_schema_to_schedule_dict(homeroom_schema: HomeroomSchema) -> dict:
    result = {}

    for homeroom in homeroom_schema.homerooms:
        name = homeroom.name
        schedule = homeroom.schedule

        list = {
            day["day"]: list(range(1, day["lastPeriod"])) for day in schedule
        }

        result[name] = list

    return result
