# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-21 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='desc',
            field=models.CharField(default='Blah blah Blah', max_length=255),
            preserve_default=False,
        ),
    ]