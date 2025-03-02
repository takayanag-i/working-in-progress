from opts.constraints.credit import CreditConstraint
from opts.constraints.homeroom import HomeroomConstraint
from opts.constraints.course import CourseConstraint
from opts.constraints.block import BlockConstraint
from opts.constraints.teacher import TeacherConstraint
from opts.constraints.consecutive_period import ConsecutivePeriodConstraint
from opts.constraints.courses_per_day import CoursesPerDayConstraint


CONSTRAINT_TYPES = {
    "HOMEROOM": HomeroomConstraint,
    "COURSE": CourseConstraint,
    "CREDIT": CreditConstraint,
    "BLOCK": BlockConstraint,
    "TEACHER": TeacherConstraint,
    "CONSECUTIVE_PERIOD": ConsecutivePeriodConstraint,
    "COURSES_PER_DAY": CoursesPerDayConstraint,
}
