# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-03 20:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0002_auto_20170427_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(
                editable=False,
                help_text='antares.apps.message.models.message.author_help',
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='antares.apps.message.models.message.author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='creation_date',
            field=models.DateTimeField(
                editable=False,
                help_text=
                'antares.apps.message.models.message.creation_name_help',
                verbose_name='antares.apps.message.models.message.creation_name'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='update_date',
            field=models.DateTimeField(
                editable=False,
                help_text=
                'antares.apps.message.models.message.update_date_help',
                verbose_name='antares.apps.message.models.message.update_date'
            ),
            preserve_default=False,
        ),
    ]
