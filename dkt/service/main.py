# coding=utf-8
import json

from django.db.models import Q
from django.forms import model_to_dict

from dkt.const import ObjectStatus, CourseStatus, UserRole
from dkt.database.models import COURSE
from dkt.service.common import random_str
from dkt.service.utils import get_user_role


def search_my_courses(request):
    """
    模糊查询我的课程
    :param request:
    """
    account = request.GET.get('account')
    field = request.GET.get('field')
    courses = [course.info for course in COURSE.objects.filter(s_account=account, info__contains=field)]
    return courses


def search_public_courses(request):
    """
    查询公开课程
    :param request:
    """
    all_courses = {}
    query = Q(s_account=ObjectStatus.UNDEFINED.value) | Q(t_account=ObjectStatus.UNDEFINED.value)
    courses = COURSE.objects.filter(query)
    for course in courses:
        if not all_courses.get(course.category):
            all_courses[course.category] = []
        all_courses[course.category].append(model_to_dict(course))
    return all_courses


def publish_course(request, post_data):
    """
    学生发布课程任务
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    role = get_user_role(account)
    data = post_data.get('course_info', {})
    data['course_id'] = random_str(8)
    data['status'] = CourseStatus.NOT_START.value
    data["info"] = json.dumps(data.get('info', {}))
    data['s_account'] = account if role == UserRole.STUDENT.value else ObjectStatus.UNDEFINED.value
    data['t_account'] = account if role == UserRole.TEACHER.value else ObjectStatus.UNDEFINED.value
    return ObjectStatus.SUCCESS.value if COURSE.objects.create(**data) else ObjectStatus.FAILED.value


def check_course(request, post_data):
    """
    认领课程
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    course_id = post_data.get("course_id")
    role = get_user_role(account)
    query = Q(course_id=course_id)
    if role == UserRole.STUDENT.value:
        status = COURSE.objects.select_for_update().filter(
            query and Q(s_account=ObjectStatus.UNDEFINED.value)).update(s_account=account)
    else:
        status = COURSE.objects.select_for_update().filter(
            query and Q(t_account=ObjectStatus.UNDEFINED.value)).update(t_account=account)
    return ObjectStatus.SUCCESS.value if status else ObjectStatus.FAILED.value
