# coding=utf-8
from dkt.const import ObjectStatus
from dkt.database.models import COURSE


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
    courses = COURSE.objects.filter(s_account=ObjectStatus.UNDEFINED.value)
    for course in courses:
        if not all_courses.get(course.category):
            all_courses[course.category] = []
        all_courses[course.category].append(course.info)
    return all_courses
