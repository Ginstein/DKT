# coding=utf-8
import time

from django.core.exceptions import ValidationError

from dkt.database.models import USERS
from dkt.service.common import random_str, md5_hash, str_to_int, int_to_str


def ping(request):
    """
    测试接口
    :return:
    """
    return True


def get_access_key(request):
    """

    :param request:
    """
    account = request.GET.get('account')
    _t = int(time.time())
    user = USERS.objects.filter(account=account, _t__lt=_t - 5)
    if not user:
        raise ValidationError('account does not exist or frequent operation')
    access_key = random_str(32)
    user.update(access_key=access_key, _t=_t)
    return {
        'access_key': access_key
    }


def get_token(request, post_data):
    """
    获取令牌
    :param request:
    :param post_data:
    :return:
    """
    account = post_data.get('account', '')
    access_key = post_data.get('access_key', '')
    enc = post_data.get('enc', '')
    nonce = post_data.get('nonce', '')
    _t = post_data.get('_t', '')
    user = USERS.objects.filter(account=account)
    if not user:
        raise ValidationError('account does not exist')
    if user.first().access_key != access_key:
        raise ValidationError('access_key expired')
    _key = account + user.first().password + access_key + str(nonce) + str(_t)
    if md5_hash(_key) != enc:
        raise ValidationError('wrong password')
    token = random_str(40)
    user.update(token=token)
    return token


def modify_password(request, post_data):
    """
    修改密码
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    token = post_data.get('token')
    enc_password = post_data.get('enc_password')
    user = USERS.objects.filter(account=account).first()
    old_password = user.password
    user.password = int_to_str(str_to_int(token) ^ str_to_int(old_password) ^ enc_password)
    # 重置token
    user.token = random_str(40)
    user.save()
    return 'Successfully modify your password, please login again'
