# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 04:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flow', '0002_auto_20170427_0107'),
        ('message', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0002_auto_20170427_0107'),
        ('document', '0002_auto_20170427_0107'),
        ('core', '0002_auto_20170427_0107'),
        ('client', '0002_auto_20170427_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagestatus',
            name='author',
            field=models.ForeignKey(
                editable=False,
                help_text=
                'antares.apps.message.models.message_status.author_help',
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='antares.apps.message.models.message_status.author'
            ), ),
        migrations.AddField(
            model_name='messagestatus',
            name='core_object',
            field=models.ForeignKey(
                db_column='message',
                on_delete=django.db.models.deletion.PROTECT,
                related_name='status_set',
                to='message.Message'), ),
        migrations.AddField(
            model_name='message',
            name='account_type',
            field=models.ForeignKey(
                blank=True,
                db_column='account_type',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='accounting.AccountType'), ),
        migrations.AddField(
            model_name='message',
            name='client',
            field=models.ForeignKey(
                blank=True,
                db_column='client',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='client.Client'), ),
        migrations.AddField(
            model_name='message',
            name='concept_type',
            field=models.ForeignKey(
                blank=True,
                db_column='concept_type',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='core.ConceptType'), ),
        migrations.AddField(
            model_name='message',
            name='document',
            field=models.ForeignKey(
                blank=True,
                db_column='document',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='document.DocumentHeader'), ),
        migrations.AddField(
            model_name='message',
            name='flow_case',
            field=models.ForeignKey(
                blank=True,
                db_column='flow_case',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='flow.FlowCase'), ),
        migrations.AddField(
            model_name='message',
            name='flow_definition',
            field=models.ForeignKey(
                blank=True,
                db_column='flow_definition',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='flow.FlowDefinition'), ),
        migrations.AddField(
            model_name='message',
            name='form_definition',
            field=models.ForeignKey(
                blank=True,
                db_column='form_definition',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='document.FormDefinition'), ),
    ]
