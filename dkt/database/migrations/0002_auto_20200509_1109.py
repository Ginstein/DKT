# Generated by Django 3.0.1 on 2020-05-09 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='_t',
            field=models.IntegerField(default=1589022546),
        ),
    ]
