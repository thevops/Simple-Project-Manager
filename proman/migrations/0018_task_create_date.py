# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('proman', '0017_auto_20161228_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data utworzenia'),
            preserve_default=False,
        ),
    ]