# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-02 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_auto_20180116_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='glaccounttype',
            name='is_document_based',
            field=models.BooleanField(default=False),
        ),
    ]