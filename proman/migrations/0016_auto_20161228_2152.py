# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-28 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proman', '0015_auto_20161222_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['enddate'], 'verbose_name_plural': 'projekty'},
        ),
        migrations.AlterField(
            model_name='task',
            name='weight',
            field=models.IntegerField(default=0, verbose_name='waga zadania'),
        ),
    ]