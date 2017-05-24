# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 04:07
from __future__ import unicode_literals

from ..constants import *
from antares.apps.core.constants import *
import ckeditor.fields
from django.db import migrations, models
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='NotificationRecord',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False)),
                ('content', models.CharField(max_length=2000)),
                ('title', models.CharField(max_length=2000)),
                ('status', enumfields.fields.EnumField(
                    default='Posted',
                    enum=NotificationStatusType,
                    max_length=30)),
                ('update_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField()),
                ('post_date', models.DateTimeField()),
            ],
            options={
                'verbose_name':
                'antares.apps.notifications.models.notification_record.table_name',
                'db_table':
                'not_record',
                'verbose_name_plural':
                'antares.apps.notifications.models.notification_record.table_name_plural',
            }, ),
        migrations.CreateModel(
            name='NotificationRule',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False)),
                ('user_code_variable', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('date_variable', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('content_variable', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('content_template', ckeditor.fields.RichTextField(
                    blank=True, null=True)),
                ('title_variable', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('update_date', models.DateTimeField(editable=False)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('active', models.BooleanField(default='true')),
            ],
            options={
                'verbose_name':
                'antares.apps.notifications.models.notification_rule.table_name',
                'db_table':
                'not_rule',
                'verbose_name_plural':
                'antares.apps.notifications.models.notification_rule.table_name_plural',
            }, ),
    ]
