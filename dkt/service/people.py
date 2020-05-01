# coding=utf-8
import json

from dkt.database.models import USERS
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
