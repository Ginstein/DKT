# Generated by Django 3.0.1 on 2020-05-09 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='COURSE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(default='', max_length=64)),
                ('s_account', models.CharField(default='', max_length=64)),
                ('t_account', models.CharField(default='', max_length=64)),
                ('category', models.CharField(default='default', max_length=64)),
                ('status', models.CharField(default='', max_length=64)),
                ('info', models.CharField(default='', max_length=2048)),
                ('start_time', models.IntegerField(default=0)),
                ('finish_time', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '课程表',
                'db_table': 'dkt_course',
            },
        ),
        migrations.CreateModel(
            name='MESSAGE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(default='', max_length=64)),
                ('t_account', models.CharField(default='', max_length=64)),
                ('receiver', models.CharField(default='all', max_length=64)),
                ('_t', models.IntegerField(default=1589022197)),
                ('msg', models.CharField(default='', max_length=2048)),
            ],
            options={
                'verbose_name': '消息表',
                'db_table': 'dkt_message',
                'ordering': ('-_t',),
            },
        ),
        migrations.CreateModel(
            name='USERS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(default='', max_length=64)),
                ('password', models.CharField(default='', max_length=64)),
                ('access_key', models.CharField(default='', max_length=128)),
                ('token', models.CharField(default='', max_length=128)),
                ('info', models.CharField(default='', max_length=2048)),
                ('_t', models.IntegerField(default=0)),
                ('role', models.CharField(default='student', max_length=16)),
            ],
            options={
                'verbose_name': '用户数据表',
                'db_table': 'dkt_users',
            },
        ),
    ]
