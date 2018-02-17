# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-14 16:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170427_0107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressitem',
            options={
                'verbose_name': 'Dirección',
                'verbose_name_plural': 'Direcciones'
            },
        ),
        migrations.AlterModelOptions(
            name='attributedefinition',
            options={
                'verbose_name': 'Definición de Atributo',
                'verbose_name_plural': 'Definiciones de Atributo'
            },
        ),
        migrations.AlterModelOptions(
            name='client',
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes'
            },
        ),
        migrations.AlterModelOptions(
            name='clientbranch',
            options={
                'verbose_name': 'Establecimiento',
                'verbose_name_plural': 'Establecimientos'
            },
        ),
        migrations.AlterModelOptions(
            name='clientbusinessclassification',
            options={
                'verbose_name': 'Clasificación de negocios de cliente',
                'verbose_name_plural': 'Clasificaciones de negocios de cliente'
            },
        ),
        migrations.AlterModelOptions(
            name='clientidentificationtype',
            options={
                'verbose_name': 'Tipo de Identificación',
                'verbose_name_plural': 'Tipos de Identificación'
            },
        ),
        migrations.AlterModelOptions(
            name='clienttype',
            options={
                'verbose_name': 'Tipo de Cliente',
                'verbose_name_plural': 'Tipos de Cliente'
            },
        ),
        migrations.AlterModelOptions(
            name='emailitem',
            options={
                'verbose_name': 'Correo Electrónico',
                'verbose_name_plural': 'Correos Electrónicos'
            },
        ),
        migrations.AlterModelOptions(
            name='identificationitem',
            options={
                'verbose_name': 'Identificación de Cliente',
                'verbose_name_plural': 'Identificaciones de Cliente'
            },
        ),
        migrations.AlterModelOptions(
            name='isicposition',
            options={
                'verbose_name': 'Posición ISIC',
                'verbose_name_plural': 'Posiciones ISIC'
            },
        ),
        migrations.AlterModelOptions(
            name='socialnetworkitem',
            options={
                'verbose_name': 'Red social de Cliente',
                'verbose_name_plural': 'Redes sociales de Cliente'
            },
        ),
        migrations.AlterModelOptions(
            name='telephoneitem',
            options={
                'verbose_name': 'Teléfono de Cliente',
                'verbose_name_plural': 'Teléfonos de Cliente'
            },
        ),
    ]
