# coding=utf-8
import json
import time

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import model_to_dict

from dkt.const import ObjectStatus, CourseStatus, UserRole
from dkt.database.models import COURSE
from dkt.database.models import PENDING
from dkt.service.common import random_str
from dkt.service.utils import get_user_role


def search_my_courses(request):
    """
    模糊查询我的课程
    :param request:
    """
    account = request.GET.get('account')
    field = request.GET.get('field', '{')
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


def get_introduction(request):
    """
    查询课程介绍
    :param request:
    :return:
    """
    course_id = request.GET.get("course_id")
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError("error course_id")
    info = json.loads(course.info)
    if 'introduction' in info:
        return info['introduction']
    else:
        raise ValidationError("has no introduction")


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


def publish_homework(request, post_data):
    """
    老师发布作业
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    course_id = post_data.get('course_id')
    tasks = post_data.get('task')
    role = get_user_role(account)
    if role != UserRole.TEACHER.value:
        raise ValidationError('only teacher can publish homework')
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError('course id does not exist')
    homework = json.loads(course.homework)
    if not homework.get('task'):
        # 初始化作业表
        homework['task'] = []
        homework['status'] = CourseStatus.NOT_START.value
        homework['start_time'] = post_data.get('start_time', int(time.time()))
        homework['finish_time'] = post_data.get('finish_time', int(time.time()))
    homework['task'] += tasks
    course.homework = json.dumps(homework)
    course.save()
    return ObjectStatus.SUCCESS.value


def get_homework(request, post_data):
    """
    老师或学生获取作业
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    course_id = post_data.get('course_id')
    role = get_user_role(account)
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError('course id does not exist')
    homework = json.loads(course.homework)
    if role == UserRole.STUDENT.value and homework['start_time'] > int(time.time()):
        raise ValidationError('the homework has not started')
    if homework['status'] == CourseStatus.NOT_START.value:
        homework['status'] = CourseStatus.ONGOING.value
    if homework['finish_time'] <= int(time.time()):
        homework['status'] = CourseStatus.FINISH.value
    homework = json.dumps(homework)
    if course.homework != homework:
        course.homework = homework
        course.save()
    return homework


def correct_homework(request, post_data):
    """
    老师批改作业
    :param request:
    :param post_data:
    """
    account = post_data.get('account')
    course_id = post_data.get('course_id')
    score = post_data.get('score')
    role = get_user_role(account)
    if role != UserRole.TEACHER.value:
        raise ValidationError('only teacher can correct homework')
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError('course id does not exist')
    homework = json.loads(course.homework)
    if homework['finish_time'] >= int(time.time()):
        raise ValidationError('the homework is not over yet')
    homework['score'] = score
    course.homework = json.dumps(homework)
    course.save()
    return ObjectStatus.SUCCESS.value


def course_evaluate(request, post_data):
    """
    课程评价
    :param request:
    :param post_data:
    :return:
    """
    evaluation = post_data.get("evaluation")
    grade = post_data.get("grade")
    course_id = post_data.get("course_id")
    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError('course does not exist')
    info = json.loads(course.info)
    info['evaluation'] = evaluation
    info['grade'] = grade
    course.info = json.dumps(info)
    course.save()
    return ObjectStatus.SUCCESS.value


def get_evaluation(request):
    """
    查看课程评价
    :param request:
    :return:
    """
    course_id = request.GET.get("course_id")
    t_id = request.GET.get("account")
    result = []
    if course_id:
        course = COURSE.objects.filter(course_id=course_id).first()
        if not course:
            raise ValidationError('course does not exist')
        info = json.loads(course.info)
        if 'evaluation' in info:
            dic = {'evaluation': info['evaluation'], 'grade': info['grade']}
        result.append(dic)
        return result
    elif t_id:
        courses = COURSE.objects.filter(t_account=t_id)
        if not courses:
            raise ValidationError('teacher does not exist')
        for ob in courses:
            info = ob.info
            if info:
                info = json.loads(info)
            if 'evaluation' in info:
                dic = {'evaluation': info['evaluation'], 'grade': info['grade'], 'account': ob.s_account,
                       'period': ob.total_periods, 'title': info['title']}
                result.append(dic)
        return result
    else:
        raise ValidationError("lack right course_id or account")


def apply_alter(request, post_data):
    """
    申请课程（建立或修改）
    :param request:
    :param post_data:
    :return:
    """
    account = post_data.get("account")
    course_id = post_data.get("course_id")
    info = post_data.get("info")

    course = COURSE.objects.filter(course_id=course_id).first()
    if not course:
        raise ValidationError('course does not exist')

    if account == course.t_account:
        another = course.s_account

    elif account == course.s_account:
        another = course.t_account
    else:
        raise ValidationError('error account')

    pending = PENDING.objects.create(course_id=course_id, applicant_id=account,
                                     another_id=another, _t=time.time(), info=json.dumps(info))
    pending.save()
    return ObjectStatus.SUCCESS.value


def search_pending(request, post_data):
    """
    查找和自己有关的请求
    :param request:
    :param post_data:
    :return:
    """
    re = []
    account = post_data.get("account")
    obj = PENDING.objects.filter(Q(another_id=account) | Q(applicant_id=account))
    obj1 = obj.filter(another_id=account, another_op='').order_by("-_t")
    re.append("need my opinion")
    for ob in obj1:
        dic = {"course_id": ob.course_id, "info": ob.info, "applicant": ob.applicant_id}
        re.append(dic)
    re.append("my pending")
    obj2 = obj.filter(applicant_id=account).order_by("-_t")
    for ob in obj2:
        if get_user_role(ob.another_id) == UserRole.STUDENT.value:
            dic = {"course_id": ob.course_id, "student_op": ob.another_op, "admin_op": ob.admin_op}
        else:
            dic = {"course_id": ob.course_id, "teacher_op": ob.another_op, "admin_op": ob.admin_op}
        re.append(dic)
    return re


def agree_alter(request, post_data):
    """
    同意课程操作
    :param request:
    :param post_data:
    :return:
    """
    course_id = post_data.get("course_id")
    opinion = post_data.get("opinion")
    account = post_data.get("account")
    course = PENDING.objects.filter(course_id=course_id).order_by("-_t").first()
    if account != course.another_id:
        raise ValidationError("error account")
    course.another_op = opinion
    course.save()
    return ObjectStatus.SUCCESS.value

