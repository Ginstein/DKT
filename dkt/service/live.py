# coding=utf-8
"""
视频业务相关支持
"""
import time

from django.core.exceptions import ValidationError

from dkt.const import *
from dkt.database.models import COURSE


def polling_time(request, post_data):
    """
    轮询课程时间
    :param post_data:
    :param request:
    """
    course_id = post_data.get('course_id')
    s_account = post_data.get('s_account')
    t_account = post_data.get('t_account')
    tot_time = post_data.get('tot_time', 60 * 40)
    is_start = post_data.get('is_start', False)
    if not (course_id and s_account):
        raise ValidationError('missing parameter')
    course = COURSE.objects.filter(course_id=course_id, s_account=s_account, t_account=t_account).first()
    if not course:
        raise ValidationError('course does not exist')
    # 课程未开始
    cur_time = int(time.time())
    if course.status == CourseStatus.NOT_START.value and is_start:
        course.status = CourseStatus.ONGOING.value
        course.start_time = cur_time
        course.tot_time = tot_time
        course.finish_time = cur_time + tot_time
    # 课程结束
    elif cur_time >= course.finish_time:
        course.status = CourseStatus.FINISH.value
    course.save()
    return {
        'course_id': course_id,
        's_account': s_account,
        't_account': t_account,
        'status': course.status,
        'color': ObjectColor[course.status].value,
        'time': time.strftime("%Y%m%d-%H:%M:%S", time.localtime(cur_time))
    }
