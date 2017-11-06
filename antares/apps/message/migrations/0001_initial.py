# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 04:07
from __future__ import unicode_literals

from ..constants import *
from antares.apps.core.constants import *
from django.db import migrations, models
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False)),
                ('period', models.IntegerField(blank=True, null=True)),
                ('message_type', enumfields.fields.EnumField(
                    enum=MessageType, max_length=30)),
                ('content', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name':
                'antares.apps.message.models.message.table_name',
                'db_table':
                'msg_message',
                'verbose_name_plural':
                'antares.apps.message.models.message.table_name_plural',
            },
        ),
        migrations.CreateModel(
            name='MessageStatus',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    primary_key=True,
                    serialize=False)),
                ('module', enumfields.fields.EnumField(
                    enum=SystemModuleType, max_length=30)),
                ('status', enumfields.fields.EnumField(
                    default='Pending', enum=MessageStatusType, max_length=30)),
                ('creation_date', models.DateTimeField(
                    editable=False,
                    help_text=
                    'antares.apps.message.models.message_status.creation_name_help',
                    verbose_name=
                    'antares.apps.message.models.message_status.creation_name')
                 ),
                ('update_date', models.DateTimeField(
                    editable=False,
                    help_text=
                    'antares.apps.message.models.message_status.update_date_help',
                    verbose_name=
                    'antares.apps.message.models.message_status.update_date')),
            ],
            options={
                'verbose_name':
                'antares.apps.message.models.message_status.table_name',
                'db_table':
                'msg_message_status',
                'verbose_name_plural':
                'antares.apps.message.models.message_status.table_name_plural',
            },
        ),
    ]
