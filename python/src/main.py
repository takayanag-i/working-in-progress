from fastapi import FastAPI
from routers.timetable import router as timetable_router


app = FastAPI()

app.include_router(timetable_router)
