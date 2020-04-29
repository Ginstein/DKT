# coding=utf-8
import functools
import json
from django.http import HttpResponse

from dkt.const import ObjectStatus


def rest_view(func):
    """
    格式化请求结果
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            result = dict(
                code=200,
                message=ObjectStatus.SUCCESS.value,
                data=func(request, *args, **kwargs)
            )
        except Exception as e:
            result = dict(
                code=500,
                message=ObjectStatus.FAILED.value,
                data=e.message
            )
        return get_json_response(request, result)

    return wrapper


def post_format(func):
    """
    接收POST请求
    :param func:
    :return:
    """

    def wrapper(request, *args, **kw):
        try:
            post_data = json.loads(str(request.body, encoding='utf-8'))
        except Exception as e:
            post_data = {}
        return func(request, post_data, *args, **kw)

    return wrapper


def get_json_response(request, content, *args, **kwargs):
    """

    :param request:
    :param content:
    :param args:
    :param kwargs:
    :return:
    """
    jsonp_callback = request.GET.get('callback')
    if jsonp_callback:
        json_ = "%s(%s)" % (jsonp_callback, json.dumps(content))
    else:
        json_ = json.dumps(content)
    response = HttpResponse(json_, 'application/json', *args, **kwargs)
    return response
