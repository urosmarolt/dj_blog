# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20160514_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='meta_description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='meta_keywords',
            field=models.CharField(default='keywords', max_length=200),
            preserve_default=False,
        ),
    ]
