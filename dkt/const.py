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


class FileSuffix(Enum):
    PDF = u'.pdf'
    PPT = u'.ppt'
    PPTX = u'.pptx'
    JPG = u'.jpg'
    PNG = u'.png'
    PICTURE = u'.jpg'  # linux
    # PICTURE = u' .jpg'  # windows


class Time(Enum):
    ADay = 86400
    JETLAG = 28800
    DAYS = 3
    INTERVAL = 1

class MessageObjects(Enum):
    RECEIVER_ALL = u'all'
    COURSE = u'course'
    SYSTEM = u'system'
    GET_MSG_NUM = 20

class UserRole(Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'
    PARENT = 'parent'
    ADMIN = 'admin'
