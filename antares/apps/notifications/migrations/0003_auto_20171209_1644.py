# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20170427_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationrule',
            name='form_definition',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='notification_rule_set',
                to='document.FormDefinition'),
        ),
    ]
