# coding=utf-8
"""
自定义工具存放位置
"""
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


def int_to_str(num):
    """
    十进制转十六进制
    :param num:
    :return:
    """
    return bytes().fromhex(str(hex(num))[2:]).decode()


def str_to_int(_str):
    """
    字符串转数字
    :param _str:
    """
    return int(_str.encode().hex(), 16)
