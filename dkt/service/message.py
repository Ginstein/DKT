# coding=utf-8
"""
用户消息接收和发布
"""

import time
from django.db.models import Q

from dkt.database.models import MESSAGES, USERS, COURSE
from dkt.const import ObjectStatus, MessageObjects

def get_message(request, post_data):
    """
    获取对话列表, 或者历史公告
    :param request:
    :param post_data:
    """

    receiver = post_data.get('account')
    course_id = post_data.get('course_id')
    since = post_data.get('since', int(time.time()))
    sender = post_data.get('sender')

    if sender == MessageObjects.PUB.value:
        msgs = MESSAGES.objects.filter(course_id=course_id, receiver=MessageObjects.ALL.value, _t__lte=since)[:10]
    else:
        msgs = MESSAGES.objects.filter(course_id=course_id, sender=sender, receiver=receiver, _t__lte=since)[:10]

    res = []
    for msg in msgs:
        res.append({'_t': msg._t, 'msg': msg.msg, 'sender': msg.sender})
    return res

def pub_message(request, post_data):
    """
    老师发布消息
    :param request:
    :param post_data:
    """

    course_id = post_data.get('course_id')
    sender = post_data.get('account')
    receiver = post_data.get('receiver')
    msg = post_data.get('msg')

#      if not COURSE.objects.filter(Q(course_id=course_id), Q(t_account=sender)|Q(s_account=sender)):
        #  return "Course and sender can't match!"
    #  if receiver != 'all' and not COURSE.objects.filter(Q(course_id=course_id), Q(t_account=receiver)|Q(s_account=receiver)):
        #  return "Course and receiver can't match!"
    #  if receiver == 'all' and USERS.objects.get(account=sender).role != 'teacher':
        #  return "Can't send to all, because you are not a teacher!"

    MESSAGES.objects.create(course_id=course_id, sender=sender, receiver=receiver, _t=int(time.time()), msg=msg)

    return ObjectStatus.SUCCESS.value
