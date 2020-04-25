# coding=utf-8
import hashlib
import random
import string


def random_str(num):
    """
    生成随机字符串
    :param num: 长度
    :return:
    """
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))

    return salt


def md5_hash(_str):
    """
    HASH
    :param _str:
    """
    md = hashlib.md5()
    md.update(_str.encode('utf-8'))
    return md.hexdigest()
