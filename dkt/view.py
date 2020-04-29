# coding=utf-8
"""
视图层url调用函数必须在这
"""
from dkt.rest.decorators import rest_view, post_format
from dkt.service.live import *
from dkt.service.login import *


# login 界面
# ==========================================
@rest_view
def Ping(request):
    return ping(request)


@rest_view
def GetAccessKey(request):
    return get_access_key(request)


@post_format
@rest_view
def GetToken(request, post_data):
    return get_token(request, post_data)


# live 界面
# ==========================================
@post_format
@rest_view
def PollingTime(request, post_data):
    return polling_time(request, post_data)
