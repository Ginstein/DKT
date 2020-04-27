# coding=utf-8
"""
视频业务相关支持
"""
import logging
import tempfile
import time
import os

from django.core.exceptions import ValidationError

from dkt.const import *
from dkt.database.models import COURSE


def polling_time(request):
    """
    轮询课程时间
    :param post_data:
    :param request:
    """
    course_id = request.GET.get('course_id')
    s_account = request.GET.get('s_account')
    t_account = request.GET.get('t_account')
    tot_time = request.GET.get('tot_time', 60 * 40)
    is_start = request.GET.get('is_start', False)
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


def ppt_to_jpg(request, post_data):
    """
     ppt转换成jpg格式
    :param request:
    :param post_data:
    :return:
    """
    ppt_name = post_data.get("ppt_name")
    ppt_path = post_data.get("ppt_path")
    if not (ppt_name and ppt_path):
        raise ValidationError('missing parameter')
    suffix = ppt_name[ppt_name.find('.'):]
    if suffix not in [FileSuffix.PPT.value, FileSuffix.PPTX.value]:
        raise ValidationError('File type error')
    try:
        # 先将ppt或pptx转化成pdf
        os.chdir(ppt_path)
        os.system("unoconv -f pdf " + ppt_name)  # linux
        # os.system("soffice --headless --convert-to pdf " + ppt_name)  # windows
        file_name = ppt_name[:ppt_name.find('.')]
        # 新建ppt名称的文件夹
        os.system("mkdir " + file_name)
        in_path = os.path.join(ppt_path, file_name + FileSuffix.PDF.value)
        out_path = os.path.join(ppt_path, os.path.join(file_name, FileSuffix.PICTURE.value))
        # TODO 把pdf转成图片放到文件夹下
        os.system("convert -resize 1200x -density 120 -quality 100 " + in_path + ' ' + out_path)  # linux
        # os.system('magick "' + in_path + '" "' + out_path + '"')  # windows
    except Exception as e:
        logger.error('ppt to jpg error {}'.format(e))
        return ObjectStatus.FAILED.value
    return ObjectStatus.SUCCESS.value


logger = logging.getLogger(__name__)