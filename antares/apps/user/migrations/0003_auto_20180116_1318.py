# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 16:18
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20171209_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.Application'),
        ),
        migrations.AlterField(
            model_name='orgunit',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.OrgUnit'),
        ),
        migrations.AlterField(
            model_name='role',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='user.Role'),
        ),
    ]
