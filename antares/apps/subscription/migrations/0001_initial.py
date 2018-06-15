# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-06-14 23:29
from __future__ import unicode_literals

from ..constants import *
from antares.apps.core.constants import *
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionAction',
            fields=[
                ('id',
                 models.UUIDField(
                     default=uuid.uuid4,
                     editable=False,
                     primary_key=True,
                     serialize=False)),
                ('order_number', models.IntegerField(blank=True, null=True)),
                ('action_definition',
                 models.ForeignKey(
                     db_column='action_definition',
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='subscription_action_set',
                     to='core.ActionDefinition')),
            ],
            options={
                'verbose_name':
                'antares.apps.subscription.models.subscription_action.table_name',
                'verbose_name_plural':
                'antares.apps.subscription.models.subscription_action.table_name_plural',
                'db_table':
                'subs_action',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionActionParameterMap',
            fields=[
                ('id',
                 models.UUIDField(
                     default=uuid.uuid4,
                     editable=False,
                     primary_key=True,
                     serialize=False)),
                ('content_text',
                 models.CharField(blank=True, max_length=255, null=True)),
                ('parameter_name',
                 models.CharField(blank=True, max_length=255, null=True)),
                ('parameter_definition',
                 models.ForeignKey(
                     blank=True,
                     db_column='parameter_definition',
                     null=True,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='subscription_action_parameter_map_set',
                     to='core.ActionParameterDefinition')),
                ('subscription_action',
                 models.ForeignKey(
                     blank=True,
                     db_column='subscription_action',
                     null=True,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='parameter_set',
                     to='subscription.SubscriptionAction')),
            ],
            options={
                'verbose_name':
                'antares.apps.subscription.models.subscription_action_parameter_map.table_name',
                'verbose_name_plural':
                'antares.apps.subscription.models.subscription_action_parameter_map.table_name_plural',
                'db_table':
                'subs_action_parameter_map',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionEvent',
            fields=[
                ('id',
                 models.UUIDField(
                     default=uuid.uuid4,
                     editable=False,
                     primary_key=True,
                     serialize=False)),
                ('script_engine', models.CharField(max_length=255)),
                ('condition_text',
                 models.CharField(blank=True, max_length=4000, null=True)),
                ('event_type',
                 enumfields.fields.EnumField(enum=EventType, max_length=30)),
                ('subscription_id', models.CharField(max_length=255)),
                ('source',
                 models.ForeignKey(
                     blank=True,
                     db_column='source',
                     null=True,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='source_event_set',
                     to='message.Message')),
                ('subscriber',
                 models.ForeignKey(
                     blank=True,
                     db_column='subscriber',
                     null=True,
                     on_delete=django.db.models.deletion.PROTECT,
                     related_name='subscriber_event_set',
                     to='message.Message')),
            ],
            options={
                'verbose_name':
                'antares.apps.subscription.models.subscription_event.table_name',
                'verbose_name_plural':
                'antares.apps.subscription.models.subscription_event.table_name_plural',
                'db_table':
                'subs_event',
            },
        ),
        migrations.AddField(
            model_name='subscriptionaction',
            name='event',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='action_set',
                to='subscription.SubscriptionEvent'),
        ),
    ]
