# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-11 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_review_featured_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='meta_keywords',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='meta_keywords',
            field=models.TextField(),
        ),
    ]
