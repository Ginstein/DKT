"""dkt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from dkt.view import *

urlpatterns = [
    # 测试
    path('', Ping),
    # login 界面
    path('login/get_access_key/', GetAccessKey),
    path('login/get_token/', GetToken),
    path('login/modify_password/', ModifyPassword),
    # live 界面
    path('live/polling_time/', PollingTime),
    path('live/ppt_to_jpg/', PptToJpg),
    # people 界面
    path('people/get_user_info/', GetUserInfo),
    path('people/set_user_info/', SetUserInfo),
    # main 界面
    path('main/search_my_courses/', SearchMyCourses),
    path('main/search_public_courses/', SearchPublicCourses),
    path('people/get_schedule/', GetSchedule),
]
