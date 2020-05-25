# Generated by Django 3.0.6 on 2020-05-23 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20200510_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='PENDING',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(default='', max_length=64)),
                ('applicant_id', models.CharField(default='', max_length=64)),
                ('another_id', models.CharField(default='', max_length=64)),
                ('another_op', models.CharField(default='', max_length=8)),
                ('admin_op', models.CharField(default='', max_length=8)),
                ('info', models.CharField(default='', max_length=2048)),
                ('_t', models.IntegerField(default=1590232656)),
            ],
            options={
                'verbose_name': '申请表',
                'db_table': 'dkt_pending',
                'ordering': ('-_t',),
            },
        ),
    ]
