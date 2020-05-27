# coding=utf-8
"""
购买课程相关业务
"""

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
    dic = {"info": info, "category": category, "value": value*period}
    trolley.append(dic)
    user.save()
    return ObjectStatus.SUCCESS.value
