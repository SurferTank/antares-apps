# Generated by Django 2.2.9 on 2020-01-20 21:17

import antares.apps.core.constants
from django.db import migrations
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_auto_20180624_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttablecontent',
            name='data_type',
            field=enumfields.fields.EnumField(blank=True, enum=antares.apps.core.constants.FieldDataType, max_length=8, null=True),
        ),
    ]