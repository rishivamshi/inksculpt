# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-05-25 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180429_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
