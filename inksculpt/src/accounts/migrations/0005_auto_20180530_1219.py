# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-05-30 12:19
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_userprofile_firstname'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=accounts.models.upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
