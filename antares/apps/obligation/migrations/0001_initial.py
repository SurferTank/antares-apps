# Generated by Django 2.0.6 on 2018-06-24 20:59

from ..constants import *
from antares.apps.core.constants import *
import ckeditor.fields
from django.db import migrations, models
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientObligation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('update_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'antares.apps.obligation.models.client_obligation.table_name',
                'verbose_name_plural': 'antares.apps.obligation.models.client_obligation.table_name_plural',
                'db_table': 'obl_client_obligation',
            },
        ),
        migrations.CreateModel(
            name='ObligationRule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('base_date', models.DateTimeField()),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('obligation_condition', models.TextField(blank=True, null=True)),
                ('end_date_expression', models.TextField(blank=True, null=True)),
                ('form_condition', models.TextField(blank=True, null=True)),
                ('init_date_expression', models.TextField(blank=True, null=True)),
                ('last_run', models.DateTimeField(blank=True, editable=False, null=True)),
                ('next_run', models.DateTimeField(blank=True, editable=False, null=True)),
                ('obligation_type', enumfields.fields.EnumField(enum=ObligationType, max_length=30)),
                ('origin', enumfields.fields.EnumField(enum=ObligationOriginType, max_length=30)),
                ('periodicity_type', enumfields.fields.EnumField(enum=ObligationPeriodicityType, max_length=30)),
                ('script_engine_type', enumfields.fields.EnumField(enum=ScriptEngineType, max_length=30)),
                ('time_unit_type', enumfields.fields.EnumField(enum=TimeUnitType, max_length=30)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('update_date', models.DateTimeField(editable=False)),
                ('saturdays_are_holiday', models.BooleanField(default=False)),
                ('sundays_are_holiday', models.BooleanField(default=False)),
                ('consider_holidays', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'antares.apps.obligation.models.obligation_rule.table_name',
                'verbose_name_plural': 'antares.apps.obligation.models.obligation_rule.table_name_plural',
                'db_table': 'obl_rule',
            },
        ),
        migrations.CreateModel(
            name='ObligationVector',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('due_date', models.DateTimeField()),
                ('compliance_date', models.DateTimeField(blank=True, null=True)),
                ('period', models.IntegerField()),
                ('status', enumfields.fields.EnumField(enum=ObligationStatusType, max_length=30)),
                ('obligation_type', enumfields.fields.EnumField(enum=ObligationType, max_length=30)),
                ('status_date', models.DateTimeField()),
                ('creation_date', models.DateTimeField()),
                ('update_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'antares.apps.obligation.models.obligation_vector.table_name',
                'verbose_name_plural': 'antares.apps.obligation.models.obligation_vector.table_name_plural',
                'db_table': 'obl_vector',
            },
        ),
        migrations.CreateModel(
            name='ObligationVectorLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=30, verbose_name=ObligationStatusType)),
                ('status_date', models.DateTimeField(blank=True, null=True)),
                ('log_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'antares.apps.obligation.models.obligation_vector_log.table_name',
                'verbose_name_plural': 'antares.apps.obligation.models.obligation_vector_log.table_name_plural',
                'db_table': 'obl_vector_log',
            },
        ),
    ]
