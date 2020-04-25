# coding=utf-8
import functools
import json
from django.http import HttpResponse

SUCCESS = 'Success'
FAILED = 'Failed'


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
                message=SUCCESS,
                data=func(request, *args, **kwargs)
            )
        except Exception as e:
            result = dict(
                code=500,
                message=e.message
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
            post_data = json.loads(request.body)
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
