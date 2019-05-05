# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-28 19:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0002_auto_20190228_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='program',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='login_reg.Programs'),
        ),
    ]