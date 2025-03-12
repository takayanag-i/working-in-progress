from fastapi import FastAPI
import uvicorn
from src.routers.timetable import router as timetable_router


app = FastAPI()

app.include_router(timetable_router)

if __name__ == '__main__':
    uvicorn.run(app)
