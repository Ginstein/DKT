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
    path('api/dkt/login/get_access_key/', GetAccessKey),
    path('api/dkt/login/get_token/', GetToken),
    path('api/dkt/login/modify_password/', ModifyPassword),
    # live 界面
    path('api/dkt/live/polling_time/', PollingTime),
    path('api/dkt/live/ppt_to_jpg/', PptToJpg),
    # people 界面
    path('api/dkt/people/get_user_info/', GetUserInfo),
    path('api/dkt/people/set_user_info/', SetUserInfo),
    path('api/dkt/people/get_schedule/', GetSchedule),
    # main 界面
    path('api/dkt/main/search_my_courses/', SearchMyCourses),
    path('api/dkt/main/search_public_courses/', SearchPublicCourses),
    path('api/dkt/main/publish_course/', PublishCourse),
    path('api/dkt/main/check_course/', CheckCourse),
    path('api/dkt/main/publish_homework/', PublishHomework),
    path('api/dkt/main/get_homework/', GetHomework),
    path('api/dkt/main/correct_homework/', CorrectHomework),
    path('api/dkt/main/course_evaluate/', CourseEvaluate),
    path('api/dkt/main/apply_alter/', ApplyAlter),
    path('api/dkt/main/agree_alter/', AgreeAlter),
    path('api/dkt/main/search_pending/', SearchPending),
    # message 界面
    path('api/dkt/message/get_msg/', GetMessage),
    path('api/dkt/message/pub_msg/', PubMessage),
]
