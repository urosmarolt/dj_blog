# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 18:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_games'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Games',
            new_name='Game',
        ),
    ]
