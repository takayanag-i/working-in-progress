from cruds.constraint.interface import ConstraintRepository
from cruds.course.interface import CourseRepository
from cruds.curriculum.interface import CurriculumRepository
from cruds.homeroom.interface import HomeroomRepository
from cruds.instructor.interface import InstructorRepository
from cruds.schedule.interface import ScheduleRepository


class AnulalDataRepository:
    def __init__(self,
                 constraint_repository: ConstraintRepository,
                 course_repository: CourseRepository,
                 curriculum_repository: CurriculumRepository,
                 homeroom_repository: HomeroomRepository,
                 instructor_repository: InstructorRepository,
                 schedule_repository: ScheduleRepository):
        self.constraint = constraint_repository
        self.course = course_repository
        self.curriculum = curriculum_repository
        self.homeroom = homeroom_repository
        self.instructor = instructor_repository
        self.schedule = schedule_repository
