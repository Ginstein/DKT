# coding=utf-8
import json

from django.core.exceptions import ValidationError

from dkt.database.models import USERS
from dkt.database.models import COURSE
from django.db.models import Q
from django.forms.models import model_to_dict
from dkt.service.common import get_timetable
from dkt.const import *


def get_user_info(request, post_data):
    """
    获取用户信息接口
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    user = USERS.objects.filter(account=account).first()
    if not user:
        raise ValidationError('account does not exist')
    return user.info


def set_user_info(request, post_data):
    """
    修改用户信息接口
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    info = post_data.get('info')
    return ObjectStatus.SUCCESS.value if USERS.objects.filter(account=account).update(
        info=json.dumps(info)) else ObjectStatus.FAILED.value


def get_schedule(request, post_data):
    """
    得到近3天的课表
    :param request:
    :param post_data:
    """
    time_table = []
    dic = {}
    account = post_data.get('account')
    # 查询用户
    user = COURSE.objects.filter(Q(s_account=account) | Q(t_account=account))
    if not user:
        raise ValidationError('account does not exist')
    # 得到时间表
    get_timetable(time_table)
    # 得到用户的课表信息
    schedules = user.filter(start_time__gte=time_table[0], start_time__lt=time_table[Time.DAYS.value])
    # 按天划分课表
    for i in range(Time.DAYS.value):
        _list = []
        schedule = schedules.filter(start_time__gte=time_table[i], start_time__lt=time_table[i+1]).order_by('start_time')
        for j in schedule:
            _list.append(model_to_dict(j))
        dic[i + 1] = _list

    return dic
