from cruds.homeroom.interface import HomeroomRepository


class HomeroomRepositoryMock(HomeroomRepository):
    def find_by_ttid(self, ttid: str):
        return
