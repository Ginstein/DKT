# coding=utf-8
"""
购买课程相关业务
"""
import json

from django.core.exceptions import ValidationError
from dkt.database.models import USERS
from dkt.const import ObjectStatus


def in_trolley(request, post_data):
    """
    加入购物车
    :param request:
    :param post_data:
    :return:
    """
    account = post_data.get("account")
    value = post_data.get("value")
    period = post_data.get("period")
    info = post_data.get("info")
    category = post_data.get("category")
    if not category:
        category = "default"
    user = USERS.objects.filter(account=account).first()
    if not user:
        raise ValidationError("error account")
    trolley = user.trolley
    if trolley:
        trolley = json.loads(trolley)
    else:
        trolley = {}
    tot_value = int(value) * int(period)
    dic = {"info": info, "category": category, "tot_value": tot_value}
    i = 0
    for tro in trolley:
        i += 1
    d = "dic" + str(i)
    trolley[d] = dic
    user.trolley = json.dumps(trolley)
    user.save()
    return ObjectStatus.SUCCESS.value


def show_trolley(request):
    """
    展示购物车
    :param request:
    :return:
    """
    account = request.GET.get("account")
    user = USERS.objects.filter(account=account).first()
    if not user:
        raise ValidationError("error account")
    trolley = user.trolley
    if trolley:
        trolley = json.loads(trolley)
    return trolley


def out_trolley(request, post_data):
    """
    删除购物车
    :param request:
    :param post_data:
    :return:
    """
    account = post_data.get("account")
    array = post_data.get("array")
    user = USERS.objects.filter(account=account).first()
    if not user:
        raise ValidationError("error account")
    trolley = user.trolley
    if not trolley:
        raise ValidationError("no trolley item")
    trolley = json.loads(trolley)
    for a in array:
        d = "dic" + str(a)
        if d in trolley:
            trolley.pop(d)
    i = 0
    for dic in trolley:
        d = "dic" + str(i)
        if dic != d:
            trolley[d] = trolley.pop(dic)
        i += 1
    user.trolley = json.dumps(trolley)
    user.save()
    return ObjectStatus.SUCCESS.value


def show_checklist(request, post_data):
    """
    显示购物清单
    :param request:
    :param post_data:
    :return:
    """
    account = post_data.get("account")
    user = USERS.objects.filter(account=account).first()
    if not user:
        raise ValidationError("error account")
    checklist = user.checklist
    return checklist
