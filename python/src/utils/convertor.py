def convert_json_to_schedule_dict(json_data: dict) -> dict:
    result = {}

    # JSON データから homerooms を取得
    for homeroom in json_data.get("homerooms", []):
        name = homeroom["name"]
        schedule = homeroom["schedule"]

        # 各曜日の最終時限をもとに動的にリストを作成
        day_schedule = {
            day_data["day"].capitalize(): list(range(1, day_data["lastPeriod"] + 1))
            for day_data in schedule
        }

        # 辞書に追加
        result[name] = day_schedule

    return result
