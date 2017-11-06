# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 04:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('document', '0002_auto_20170427_0107'),
        ('flow', '0002_auto_20170427_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationrule',
            name='author',
            field=models.ForeignKey(
                db_column='author',
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificationrule',
            name='form_definition',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='notification_rule_set',
                to='document.FormDefinition'),
        ),
        migrations.AddField(
            model_name='notificationrule',
            name='target_role',
            field=models.ForeignKey(
                blank=True,
                db_column='target_role',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='user.Role'),
        ),
        migrations.AddField(
            model_name='notificationrule',
            name='target_unit',
            field=models.ForeignKey(
                blank=True,
                db_column='target_unit',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='user.OrgUnit'),
        ),
        migrations.AddField(
            model_name='notificationrule',
            name='target_user',
            field=models.ForeignKey(
                blank=True,
                db_column='target_user',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='notification_rule_target_user_set',
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificationrecord',
            name='author',
            field=models.ForeignKey(
                blank=True,
                db_column='author',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notificationrecord',
            name='document',
            field=models.ForeignKey(
                blank=True,
                db_column='document_header',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='document.DocumentHeader'),
        ),
        migrations.AddField(
            model_name='notificationrecord',
            name='flow_case',
            field=models.ForeignKey(
                blank=True,
                db_column='flow_case',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='flow.FlowCase'),
        ),
        migrations.AddField(
            model_name='notificationrecord',
            name='recipient',
            field=models.ForeignKey(
                blank=True,
                db_column='recipient',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='notification_recipient_set',
                to=settings.AUTH_USER_MODEL),
        ),
    ]
