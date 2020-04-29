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


class ObjectColor(Enum):
    NotStart = u'Gray'
    Ongoing = u'Green'
    Finish = u'Red'


class CourseStatus(Enum):
    FINISH = u'Finish'
    NOT_START = u'NotStart'
    ONGOING = u'Ongoing'
