# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_review_tracking_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_keywords',
            field=models.CharField(default='keywords', max_length=150),
            preserve_default=False,
        ),
    ]
