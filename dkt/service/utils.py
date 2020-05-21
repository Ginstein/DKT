# coding=utf-8
from dkt.const import UserRole
from dkt.database.models import USERS, COURSE


def get_user_role(account):
    """
    获取用户角色
    :param account:
    :return:
    """
    return USERS.objects.filter(account=account).first().role


def get_room_url(course_id, role):
    """
    获取直播房间地址
    :param course_id:
    :param role:
    """
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course.room_url:
        # TODO 从live侧获取一个room url
        room_url = 'http://39.97.67.70:3000/#/zh-CN/whiteboard/host/19c69690936011eaa55f91c00e8a23a4/73995/'
        course.room_url = room_url
        course.save()
    else:
        room_url = course.room_url
    return room_url
