# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-21 23:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20180214_1324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressitem',
            options={
                'verbose_name': 'Address Item',
                'verbose_name_plural': 'Address Items'
            },
        ),
        migrations.AlterModelOptions(
            name='attributedefinition',
            options={
                'verbose_name': 'Attribute Definition',
                'verbose_name_plural': 'Attribute Definitions'
            },
        ),
        migrations.AlterModelOptions(
            name='client',
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients'
            },
        ),
        migrations.AlterModelOptions(
            name='clientbranch',
            options={
                'verbose_name': 'Client Branch',
                'verbose_name_plural': 'Client Branches'
            },
        ),
        migrations.AlterModelOptions(
            name='clientbusinessclassification',
            options={
                'verbose_name': 'Client Business Classification',
                'verbose_name_plural': 'Client Business Classifications'
            },
        ),
        migrations.AlterModelOptions(
            name='clientidentificationtype',
            options={
                'verbose_name': 'Identification Type',
                'verbose_name_plural': 'Identification Types'
            },
        ),
        migrations.AlterModelOptions(
            name='clienttype',
            options={
                'verbose_name': 'Client Type',
                'verbose_name_plural': 'Client Types'
            },
        ),
        migrations.AlterModelOptions(
            name='emailitem',
            options={
                'verbose_name': 'Email Item',
                'verbose_name_plural': 'Email Items'
            },
        ),
        migrations.AlterModelOptions(
            name='identificationitem',
            options={
                'verbose_name': 'Identification Item',
                'verbose_name_plural': 'Identification Items'
            },
        ),
        migrations.AlterModelOptions(
            name='isicposition',
            options={
                'verbose_name': 'Isic Position',
                'verbose_name_plural': 'Isic Positions'
            },
        ),
        migrations.AlterModelOptions(
            name='socialnetworkitem',
            options={
                'verbose_name': 'Social Network Item',
                'verbose_name_plural': 'Social Network Items'
            },
        ),
        migrations.AlterModelOptions(
            name='telephoneitem',
            options={
                'verbose_name': 'Telephone Item',
                'verbose_name_plural': 'Telephone Items'
            },
        ),
    ]
