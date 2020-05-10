# coding=utf-8
from dkt.database.models import USERS


def get_user_role(account):
    """
    获取用户角色
    :param account:
    :return:
    """
    return USERS.objects.filter(account=account).first().role
