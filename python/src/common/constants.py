from enum import Enum

from opts.constraints.base import ConstraintBase
from opts.constraints.homeroom import HomeroomConstraint
from opts.constraints.course import CourseConstraint
from opts.constraints.credit import CreditConstraint
from opts.constraints.block import BlockConstraint
from opts.constraints.teacher import TeacherConstraint
from opts.constraints.consecutive_period import ConsecutivePeriodConstraint
from opts.constraints.courses_per_day import CoursesPerDayConstraint


class ConstraintType(Enum):
    """
    Enum for constraint types
    """
    HOMEROOM = ("homeroom", HomeroomConstraint)
    COURSE = ("course", CourseConstraint)
    CREDIT = ("credit", CreditConstraint)
    BLOCK = ("block", BlockConstraint)
    TEACHER = ("teacher", TeacherConstraint)
    CONSECTIVE_PERIOD = ("consective_period", ConsecutivePeriodConstraint)
    COURSES_PER_DAY = ("course_per_day", CoursesPerDayConstraint)

    def __init__(self, key: str, constraint_class: type):
        self.key = key
        self.constraint_class = constraint_class

    def __call__(self, **kwargs) -> ConstraintBase:
        return self.constraint_class(**kwargs)
