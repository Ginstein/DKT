# coding=utf-8
import json
import time

from django.core.exceptions import ValidationError

from dkt.database.models import USERS
from dkt.database.models import COURSE
from django.db.models import Q
from django.forms.models import model_to_dict
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
    list1 = []
    list2 = []
    list3 = []
    account = post_data.get('account')

    # 得到今天日期时间戳
    # TODO
    today_t = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d")))

    tomorrow_t = today_t + Time.aDay.value  # 明天日期时间戳
    day_after_tomorrow = tomorrow_t + Time.aDay.value  # 后天日期时间戳
    end_t = day_after_tomorrow + Time.aDay.value  # 大后天时间戳

    # 得到三天有关用户的课表信息
    user = COURSE.objects.filter(Q(s_account=account) | Q(t_account=account))
    if not user:
        raise ValidationError('account does not exist')

    schedules = user.filter(start_time__gte=today_t, start_time__lt=end_t)
    # 分别得到三天的课表
    schedule_1 = schedules.filter(start_time__gte=today_t, start_time__lt=tomorrow_t).order_by('start_time')
    schedule_2 = schedules.filter(start_time__gte=tomorrow_t, start_time__lt=day_after_tomorrow).order_by('start_time')
    schedule_3 = schedules.filter(start_time__gte=day_after_tomorrow, start_time__lt=end_t).order_by('start_time')
    # 讲课表装到链表
    for ob in schedule_1:
        list1.append(model_to_dict(ob))
    for ob in schedule_2:
        list2.append(model_to_dict(ob))
    for ob in schedule_3:
        list3.append(model_to_dict(ob))

    schedule = {1: list1, 2: list2, 3: list3}
    '''
    # test
    t_id2 = schedule[1][0]['course_id']
    for key in schedule:
        lists = schedule[key]
        for li_st in lists:
            s_id = li_st['id']
    '''
    return schedule
