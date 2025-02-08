from fastapi import APIRouter

router = APIRouter()


@router.post("api/timetable/solve")
def solve():
    return {"message": "解けました"}
