# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
