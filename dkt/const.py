# coding=utf-8
"""
管理所有常量
"""
from enum import Enum, IntEnum


class ObjectStatus(Enum):
    SUCCESS = u'Success'
    FAILED = u'Failed'
    PENDING = u'Pending'
    FINISH = u'Finish'
    UNDEFINED = u'undefined'


class ObjectColor(Enum):
    NotStart = u'Gray'
    Ongoing = u'Green'
    Finish = u'Red'


class CourseStatus(Enum):
    FINISH = u'Finish'
    NOT_START = u'NotStart'
    ONGOING = u'Ongoing'

class UserRole(Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'
    PARENT = 'parent'
    ADMIN = 'admin'
