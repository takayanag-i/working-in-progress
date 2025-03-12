from fastapi import APIRouter

router = APIRouter()


@router.get("/api")
def home():
    return {"message": "ホームです"}


@router.post("/api/solutions")
def solve():
    return {"message": "解けました"}
