# coding=utf-8
from django.db import models


# Create your models here.

class USERS(models.Model):
    class Meta:
        verbose_name = '用户数据表'
        db_table = 'dkt_users'

    account = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    access_key = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
    info = models.CharField(max_length=2048)
    _t = models.IntegerField()
