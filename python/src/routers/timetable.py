from fastapi import APIRouter

router = APIRouter()


@router.post("api/solver/{timetable_id}")
def solve(timetable_id: str):
    return {"message": "解けました",
            "時間割ID": timetable_id}
