# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160502_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_banner',
            field=models.ImageField(default='blog/static/uploads/review_banner.jpg', upload_to='blog/static/uploads'),
        ),
    ]