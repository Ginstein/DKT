# coding=utf-8
"""
视图层url调用函数必须在这
"""
from dkt.rest.decorators import *
from dkt.service.live import *
from dkt.service.login import *
from dkt.service.main import *
from dkt.service.people import *


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


@post_format
@rest_view
@permission_validation
def ModifyPassword(request, post_data):
    return modify_password(request, post_data)


# live 界面
# ==========================================
@rest_view
def PollingTime(request):
    return polling_time(request)


@post_format
@rest_view
# @permission_validation
def PptToJpg(request, post_data):
    return ppt_to_jpg(request, post_data)


# people 界面
# ==========================================
@post_format
@rest_view
@permission_validation
def GetUserInfo(request, post_data):
    return get_user_info(request, post_data)


@post_format
@rest_view
@permission_validation
def SetUserInfo(request, post_data):
    return set_user_info(request, post_data)


# main 界面
# ==========================================
@rest_view
def SearchMyCourses(request):
    return search_my_courses(request)


@rest_view
def SearchPublicCourses(request):
    return search_public_courses(request)


@post_format
@rest_view
# @permission_validation
def GetSchedule(request, post_data):
    return get_schedule(request, post_data)
