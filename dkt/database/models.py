# coding=utf-8
from django.db import models


# Create your models here.

class USERS(models.Model):
    class Meta:
        verbose_name = '用户数据表'
        db_table = 'dkt_users'

    account = models.CharField(max_length=64, default='')
    password = models.CharField(max_length=64, default='')
    access_key = models.CharField(max_length=128, default='')
    token = models.CharField(max_length=128, default='')
    info = models.CharField(max_length=2048, default='')
    _t = models.IntegerField(default=0)


class COURSE(models.Model):
    class Meta:
        verbose_name = '课程表'
        db_table = 'dkt_course'

    course_id = models.CharField(max_length=64, default='')
    s_account = models.CharField(max_length=64, default='')
    t_account = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=64, default='default')
    status = models.CharField(max_length=64, default='')
    info = models.CharField(max_length=2048, default='')
    start_time = models.IntegerField(default=0)
    finish_time = models.IntegerField(default=0)
