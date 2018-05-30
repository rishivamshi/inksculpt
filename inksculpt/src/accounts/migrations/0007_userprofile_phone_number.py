# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-05-30 16:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180530_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]
