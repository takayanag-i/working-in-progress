import json
import os
from typing import List
from cruds.constraint.interface import ConstraintRepository
from cruds.course.interface import CourseRepository
from cruds.curriculum.interface import CurriculumRepository
from cruds.homeroom.interface import HomeroomRepository
from cruds.instructor.interface import InstructorRepository
from cruds.schedule.interface import ScheduleRepository
from models.constraint import ConstraintSchema
from models.course import CourseSchema
from models.curriculum import CurriculumSchema
from models.homeroom import HomeroomSchema
from models.instructor import InstructorSchema
from models.schedule import ScheduleSchema


class BaseRepositoryMock:

    def __init__(self, resource_dir: str):
        if not resource_dir:
            raise RuntimeError("resource_dir を指定してください")

        self.resource_dir = resource_dir

    def _load_schema(self, filename: str, schema_class):
        """指定されたファイルからJSONを読み込み、スキーマクラスに変換"""
        file_path = os.path.join(self.resource_dir, filename)
        with open(file_path, "r") as file:
            data = json.load(file)
            return schema_class(**data)


class ConstraintRepositoryMock(ConstraintRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> List[ConstraintSchema]:
        pass


class CourseRepositoryMock(CourseRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> CourseSchema:
        return self._load_schema("course_schema.json", CourseSchema)


class CurriculumRepositoryMock(CurriculumRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> CurriculumSchema:
        return self._load_schema("curriculum_schema.json", CurriculumSchema)


class HomeroomRepositoryMock(HomeroomRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> HomeroomSchema:
        return self._load_schema("homeroom_schema.json", HomeroomSchema)


class InstructorRepositoryMock(InstructorRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> InstructorSchema:
        return self._load_schema("instructor_schema.json", InstructorSchema)


class ScheduleRepositoryMock(ScheduleRepository, BaseRepositoryMock):
    def find_by_ttid(self, ttid: str) -> ScheduleSchema:
        return self._load_schema("schedule_schema.json", ScheduleSchema)
