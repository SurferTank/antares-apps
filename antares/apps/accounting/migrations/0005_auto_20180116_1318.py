# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 16:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20171209_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrule',
            name='fixed_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Client'),
        ),
        migrations.AlterField(
            model_name='glaccounttype',
            name='author',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='glaccounttype',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='accounting.GLAccountType'),
        ),
    ]