# Generated by Django 3.0.4 on 2020-03-25 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0005_auto_20200308_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentheader',
            name='association_type',
            field=models.CharField(choices=[('None', 'antares.apps.document.constants.DocumentAssociationType.NONE')], default='None', help_text='antares.apps.document.models.document_header.association_type_help', max_length=30, verbose_name='antares.apps.document.models.document_header.association_type'),
        ),
    ]
