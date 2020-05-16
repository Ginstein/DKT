# coding=utf-8
"""
用户消息接收和发布
"""

import time
from django.core.exceptions import ValidationError
from django.db.models import Q

from dkt.database.models import MESSAGES
from dkt.const import ObjectStatus, MessageObjects

def get_message(request, post_data):
    """
    获取对话列表, 或者历史公告
    :param request:
    :param post_data:
    """

    communicator_1 = post_data.get('account')
    course_id = post_data.get('course_id')
    since = post_data.get('since', int(time.time()))
    communicator_2 = post_data.get('communicator')

    if communicator_2 is None:
        raise ValidationError('Missing parameters !')

    if communicator_2 == MessageObjects.SYSTEM.value:
        msgs = MESSAGES.objects.filter(
                (Q(sender=MessageObjects.SYSTEM.value)&(Q(receiver=communicator_1)|Q(receiver=MessageObjects.RECEIVER_ALL.value))) | (Q(sender=communicator_1)&Q(receiver=MessageObjects.SYSTEM.value)),
                Q(_t__lte=since),
                Q(course_id=None)
                )[:MessageObjects.GET_MSG_NUM.value]
    elif communicator_2 == MessageObjects.COURSE.value:
        msgs = MESSAGES.objects.filter(
                course_id=course_id,
                receiver=MessageObjects.RECEIVER_ALL.value,
                _t__lte=since
                )[:MessageObjects.GET_MSG_NUM.value]
    else:
        msgs = MESSAGES.objects.filter(
                (Q(sender=communicator_2)&Q(receiver=communicator_1)) | (Q(sender=communicator_1)&Q(receiver=communicator_2)),
                Q(_t__lte=since)
                )[:MessageObjects.GET_MSG_NUM.value]

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

    if not (receiver and msg):
        raise ValidationError('Missing parameters !')

    MESSAGES.objects.create(course_id=course_id, sender=sender, receiver=receiver, _t=int(time.time()), msg=msg)

    return ObjectStatus.SUCCESS.value
