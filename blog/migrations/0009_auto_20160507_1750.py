# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-07 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20160507_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='payment_methods',
        ),
        migrations.AddField(
            model_name='review',
            name='payment_methods',
            field=models.TextField(default='VISA'),
            preserve_default=False,
        ),
    ]
