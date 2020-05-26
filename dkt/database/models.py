# coding=utf-8
from django.db import models
import time

# Create your models here.


class USERS(models.Model):
    class Meta:
        verbose_name = '用户数据表'
        db_table = 'dkt_users'

    account = models.CharField(max_length=64, default='')
    password = models.CharField(max_length=64, default='')
    role = models.CharField(max_length=64, default='')
    access_key = models.CharField(max_length=128, default='')
    token = models.CharField(max_length=128, default='')
    info = models.CharField(max_length=2048, default='')
    _t = models.IntegerField(default=0)
    role = models.CharField(max_length=16, default='student')


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
    homework = models.TextField(default='')
    start_time = models.IntegerField(default=0)
    finish_time = models.IntegerField(default=0)
    total_periods = models.IntegerField(default=0)
    passed_periods = models.IntegerField(default=0)


class MESSAGES(models.Model):
    class Meta:
        verbose_name = '消息表'
        db_table = 'dkt_messages'
        ordering = ('-_t', )

    course_id = models.CharField(max_length=64, default='', null=True)
    sender = models.CharField(max_length=64, default='')
    receiver = models.CharField(max_length=64, default='')
    _t = models.IntegerField(default=int(time.time()))
    msg = models.TextField()


class PENDING(models.Model):
    class Meta:
        verbose_name = '申请表'
        db_table = 'dkt_pending'

    course_id = models.CharField(max_length=64, default='')
    applicant_id = models.CharField(max_length=64, default='')
    another_id = models.CharField(max_length=64, default='')
    another_op = models.CharField(max_length=8, default='')
    admin_op = models.CharField(max_length=8, default='')
    info = models.CharField(max_length=2048, default='')
    _t = models.IntegerField(default=int(time.time()))
