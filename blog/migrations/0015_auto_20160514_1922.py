# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-14 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20160514_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='exclusive_bonus',
            field=models.TextField(default='Exclusive bonus'),
        ),
        migrations.AlterField(
            model_name='review',
            name='freespins',
            field=models.TextField(default='Freespins'),
        ),
        migrations.AlterField(
            model_name='review',
            name='general_info',
            field=models.TextField(default='General info'),
        ),
        migrations.AlterField(
            model_name='review',
            name='match_bonus',
            field=models.TextField(default='Match bonus'),
        ),
        migrations.AlterField(
            model_name='review',
            name='meta_description',
            field=models.TextField(default='Meta Description'),
        ),
        migrations.AlterField(
            model_name='review',
            name='meta_keywords',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='payment_methods',
            field=models.TextField(default='Payment methods'),
        ),
        migrations.AlterField(
            model_name='review',
            name='ratings',
            field=models.TextField(default='Ratings'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(default='Review text'),
        ),
    ]
