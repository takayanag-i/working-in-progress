from cruds.schedule.interface import ScheduleRepository


class ScheduleRepositoryMock(ScheduleRepository):
    def find_by_ttid(self):
        return
