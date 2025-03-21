from cruds.constraint.interface import ConstraintRepository
from cruds.course.interface import CourseRepository
from cruds.curriculum.interface import CurriculumRepository
from cruds.homeroom.interface import HomeroomRepository
from cruds.instructor.interface import InstructorRepository
from cruds.schedule.interface import ScheduleRepository
from opts.anual_model import AnualModel
from opts.schema_extractor import (get_course_details,
                                   get_course_list,
                                   get_curriculums,
                                   get_day_list,
                                   get_homeroom_list,
                                   get_instructor_list,
                                   get_period_list,
                                   get_periods)
from opts.anual_executor import execute


class AnualSolverService:

    def __init__(self,
                 ttid: str,
                 constraint_repo: ConstraintRepository,
                 course_repo: CourseRepository,
                 curriculum_repo: CurriculumRepository,
                 homeroom_repo: HomeroomRepository,
                 instructor_repo: InstructorRepository,
                 schedule_repo: ScheduleRepository):
        self.constraint_repo = constraint_repo
        self.course_repo = course_repo
        self.curriculum_repo = curriculum_repo
        self.homeroom_repo = homeroom_repo
        self.instructor_repo = instructor_repo
        self.schedule_repo = schedule_repo

    def bulid_anual_model(self, ttid: str) -> AnualModel:

        course_schema = self.course_repo.find_by_ttid(ttid)
        curriculum_schema = self.curriculum_repo.find_by_ttid(ttid)
        homeroom_schema = self.homeroom_repo.find_by_ttid(ttid)
        instructor_schema = self.instructor_repo.find_by_ttid(ttid)
        schedule_schema = self.schedule_repo.find_by_ttid(ttid)

        model = AnualModel()
        model.data.H = get_homeroom_list(homeroom_schema)
        model.data.D = get_day_list(schedule_schema)
        model.data.P = get_period_list(schedule_schema)
        model.data.C = get_course_list(course_schema)
        model.data.I = get_instructor_list(instructor_schema)
        model.data.periods = get_periods(homeroom_schema)
        model.data.curriculums = get_curriculums(curriculum_schema)
        model.data.course_details = get_course_details(course_schema)

        return model

    def create_anual_timetable(self, ttid: str):
        constraint_schemas = self.constraint_repo.find_by_ttid(ttid)
        model = self.bulid_anual_model(ttid)
        solution = execute(model, constraint_schemas)

        return solution

    def insert(self, solution):
        pass
