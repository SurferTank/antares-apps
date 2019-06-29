# Generated by Django 2.0.6 on 2018-06-24 20:59

from ..constants import *
from antares.apps.core.constants import *
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentACL',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.document_acl.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.document_acl.id')),
                ('access_type', models.CharField(default=DocumentACLAccessType('None'), max_length=30, verbose_name=DocumentACLAccessType)),
                ('creation_date', models.DateTimeField(editable=False, help_text='antares.apps.document.models.document_acl.creation_name_help', verbose_name='antares.apps.document.models.document_acl.creation_name')),
                ('update_date', models.DateTimeField(editable=False, help_text='antares.apps.document.models.document_acl.update_date_help', verbose_name='antares.apps.document.models.document_acl.update_date')),
            ],
            options={
                'verbose_name': 'Document Access Control List',
                'verbose_name_plural': 'Document Access Control Lists',
                'db_table': 'doc_document_acl',
            },
        ),
        migrations.CreateModel(
            name='DocumentField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.document_field.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.document_field.id')),
                ('clob_value', models.BinaryField(blank=True, help_text='antares.apps.document.models.document_field.clob_value_help', null=True, verbose_name='antares.apps.document.models.document_field.clob_value')),
                ('data_type', enumfields.fields.EnumField(enum=FieldDataType, help_text='antares.apps.document.models.document_field.data_type_help', max_length=30, verbose_name='antares.apps.document.models.document_field.data_type')),
                ('date_value', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_field.date_value_help', null=True, verbose_name='antares.apps.document.models.document_field.date_value')),
                ('float_value', models.DecimalField(blank=True, decimal_places=2, help_text='antares.apps.document.models.document_field.float_value_help', max_digits=19, null=True, verbose_name='antares.apps.document.models.document_field.float_value')),
                ('definition', models.CharField(help_text='antares.apps.document.models.document_field.definition_help', max_length=40, verbose_name='antares.apps.document.models.document_field.definition')),
                ('integer_value', models.BigIntegerField(blank=True, help_text='antares.apps.document.models.document_field.integer_value_help', null=True, verbose_name='antares.apps.document.models.document_field.integer_value')),
                ('ordinal', models.IntegerField(default=0, help_text='antares.apps.document.models.document_field.ordinal_help', verbose_name='antares.apps.document.models.document_field.ordinal')),
                ('string_value', models.CharField(blank=True, help_text='antares.apps.document.models.document_field.string_value_help', max_length=2000, null=True, verbose_name='antares.apps.document.models.document_field.string_value')),
                ('text_value', models.TextField(blank=True, help_text='antares.apps.document.models.document_field.text_value_help', null=True, verbose_name='antares.apps.document.models.document_field.text_value')),
                ('uuid_value', models.UUIDField(blank=True, help_text='antares.apps.document.models.document_field.uuid_value_help', null=True, verbose_name='antares.apps.document.models.document_field.uuid_value')),
                ('comments', models.TextField(blank=True, help_text='antares.apps.document.models.document_field.comments_help', null=True, verbose_name='antares.apps.document.models.document_field.comments_value')),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.document_field.table_name',
                'verbose_name_plural': 'antares.apps.document.models.document_field.table_name_plural',
                'db_table': 'doc_field',
            },
        ),
        migrations.CreateModel(
            name='DocumentHeader',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.document_header.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.document_header.id')),
                ('period', models.IntegerField(blank=True, help_text='antares.apps.document.models.document_header.period_help', null=True, verbose_name='antares.apps.document.models.document_header.period')),
                ('active_version', models.BooleanField(default=True, help_text='antares.apps.document.models.document_header.active_version_help', verbose_name='antares.apps.document.models.document_header.active_version')),
                ('association_type', enumfields.fields.EnumField(default='None', enum=DocumentAssociationType, help_text='antares.apps.document.models.document_header.association_type_help', max_length=30, verbose_name='antares.apps.document.models.document_header.association_type')),
                ('cancel_date', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_header.cancel_date_help', null=True, verbose_name='antares.apps.document.models.document_header.cancel_date')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, help_text='antares.apps.document.models.document_header.creation_date_help', verbose_name='antares.apps.document.models.document_header.creation_date')),
                ('delete_date', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_header.delete_date_help', null=True, verbose_name='antares.apps.document.models.document_header.delete_date')),
                ('document_number', models.BigIntegerField(blank=True, help_text='antares.apps.document.models.document_header.document_number_help', null=True, verbose_name='antares.apps.document.models.document_header.document_number')),
                ('document_version', models.IntegerField(blank=True, help_text='antares.apps.document.models.document_header.document_version_help', null=True, verbose_name='antares.apps.document.models.document_header.document_version')),
                ('draft_date', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_header.draft_date_help', null=True, verbose_name='antares.apps.document.models.document_header.draft_date')),
                ('hash', models.CharField(blank=True, help_text='antares.apps.document.models.document_header.hash_help', max_length=100, null=True, verbose_name='antares.apps.document.models.document_header.hash')),
                ('hrn_code', models.CharField(help_text='antares.apps.document.models.document_header.hrn_code_help', max_length=255, unique=True, verbose_name='antares.apps.document.models.document_header.hrn_code')),
                ('hrn_title', models.CharField(blank=True, help_text='antares.apps.document.models.document_header.hrn_title_help', max_length=4000, null=True, verbose_name='antares.apps.document.models.document_header.hrn_title')),
                ('origin', enumfields.fields.EnumField(default='Unknown', enum=DocumentOriginType, help_text='antares.apps.document.models.document_header.origin_help', max_length=30, verbose_name='antares.apps.document.models.document_header.origin')),
                ('save_date', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_header.save_date_help', null=True, verbose_name='antares.apps.document.models.document_header.save_date')),
                ('status', enumfields.fields.EnumField(default='Drafted', enum=DocumentStatusType, help_text='antares.apps.document.models.document_header.status_help', max_length=30, verbose_name='antares.apps.document.models.document_header.status')),
                ('default_currency', models.CharField(blank=True, help_text='antares.apps.document.models.document_header.default_currency_help', max_length=30, null=True, verbose_name='antares.apps.document.models.document_header.default_currency')),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.document_header.table_name',
                'verbose_name_plural': 'antares.apps.document.models.document_header.table_name_plural',
                'db_table': 'doc_header',
            },
        ),
        migrations.CreateModel(
            name='DocumentHrn',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.document_hrn.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.document_hrn.id')),
                ('hrn_code', models.CharField(blank=True, help_text='antares.apps.document.models.document_hrn.hrn_code_help', max_length=255, null=True, verbose_name='antares.apps.document.models.document_hrn.hrn_code')),
                ('hrn_title', models.CharField(blank=True, help_text='antares.apps.document.models.document_hrn.hrn_title_help', max_length=255, null=True, verbose_name='antares.apps.document.models.document_hrn.hrn_title')),
                ('status', enumfields.fields.EnumField(default='Drafted', enum=DocumentStatusType, help_text='antares.apps.document.models.document_hrn.status_help', max_length=30, verbose_name='antares.apps.document.models.document_hrn.status')),
                ('until_date', models.DateTimeField(blank=True, help_text='antares.apps.document.models.document_hrn.until_date_help', null=True, verbose_name='antares.apps.document.models.document_hrn.until_date')),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.document_hrn.table_name',
                'verbose_name_plural': 'antares.apps.document.models.document_hrn.table_name_plural',
                'db_table': 'doc_hrn',
            },
        ),
        migrations.CreateModel(
            name='DocumentTableContent',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('clob_value', models.CharField(blank=True, max_length=255, null=True)),
                ('column_number', models.IntegerField(blank=True, null=True)),
                ('data_type', enumfields.fields.EnumField(blank=True, enum=FieldDataType, max_length=7, null=True)),
                ('date_value', models.DateTimeField(blank=True, null=True)),
                ('decimal_value', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('definition', models.CharField(blank=True, max_length=40, null=True)),
                ('integer_value', models.BigIntegerField(blank=True, null=True)),
                ('row_number', models.IntegerField(blank=True, null=True)),
                ('string_value', models.CharField(blank=True, max_length=2000, null=True)),
                ('table_definition', models.CharField(blank=True, max_length=40, null=True)),
                ('text_value', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.document_table_content.table_name',
                'verbose_name_plural': 'antares.apps.document.models.document_table_content.table_name_plural',
                'db_table': 'doc_table_contents',
            },
        ),
        migrations.CreateModel(
            name='FormActionMap',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action_type', models.CharField(max_length=255)),
                ('active', models.IntegerField(blank=True, null=True)),
                ('creation_date', models.DateTimeField()),
                ('update_date', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.form_action_map.table_name',
                'verbose_name_plural': 'antares.apps.document.models.form_action_map.table_name_plural',
                'db_table': 'doc_action_map',
            },
        ),
        migrations.CreateModel(
            name='FormClass',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('type', enumfields.fields.EnumField(default='Administrative', enum=FormClassType, max_length=30)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('status', enumfields.fields.EnumField(default='Development', enum=FormClassStatusType, max_length=30)),
                ('third_party_type', models.CharField(blank=True, db_index=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Form Class',
                'verbose_name_plural': 'Form Classes',
                'db_table': 'doc_form_class',
            },
        ),
        migrations.CreateModel(
            name='FormDefinition',
            fields=[
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('definition', models.TextField(blank=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('edit_js_xslt', models.TextField(blank=True, null=True)),
                ('edit_xslt', models.TextField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('form_name', models.CharField(editable=False, max_length=100)),
                ('form_version', models.IntegerField(default=0, editable=False)),
                ('hrn_script', models.TextField(blank=True, null=True)),
                ('print_xslt', models.TextField(blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('status', enumfields.fields.EnumField(default='Development', enum=FormDefinitionStatusType, max_length=30)),
                ('view_xslt', models.TextField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Form Definition',
                'verbose_name_plural': 'Form Definitions',
                'db_table': 'doc_form_definition',
            },
        ),
        migrations.CreateModel(
            name='FormDefinitionACL',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='antares.apps.document.model.FormDefinitionACL.id')),
                ('access_type', enumfields.fields.EnumField(default='None', enum=FormDefinitionACLAccessType, max_length=30)),
                ('creation_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('update_date', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Form Definition Access Control List',
                'verbose_name_plural': 'Form Definition Access Control Lists',
                'db_table': 'doc_form_definition_acl',
            },
        ),
        migrations.CreateModel(
            name='IndexedField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.indexed_field.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.indexed_field.id')),
                ('clob_value', models.BinaryField(blank=True, help_text='antares.apps.document.models.indexed_field.clob_value_help', null=True, verbose_name='antares.apps.document.models.indexed_field.clob_value')),
                ('data_type', enumfields.fields.EnumField(enum=FieldDataType, help_text='antares.apps.document.models.indexed_field.data_type_help', max_length=30, verbose_name='antares.apps.document.models.indexed_field.data_type')),
                ('date_value', models.DateTimeField(blank=True, db_index=True, help_text='antares.apps.document.models.indexed_field.date_value_help', null=True, verbose_name='antares.apps.document.models.indexed_field.date_value')),
                ('float_value', models.DecimalField(blank=True, db_index=True, decimal_places=2, help_text='antares.apps.document.models.indexed_field.float_value_help', max_digits=19, null=True, verbose_name='antares.apps.document.models.indexed_field.float_value')),
                ('definition', models.CharField(help_text='antares.apps.document.models.indexed_field.definition_help', max_length=40, verbose_name='antares.apps.document.models.indexed_field.definition')),
                ('integer_value', models.BigIntegerField(blank=True, db_index=True, help_text='antares.apps.document.models.indexed_field.integer_value_help', null=True, verbose_name='antares.apps.document.models.indexed_field.integer_value')),
                ('ordinal', models.IntegerField(db_index=True, default=0, help_text='antares.apps.document.models.indexed_field.ordinal_help', verbose_name='antares.apps.document.models.indexed_field.ordinal')),
                ('string_value', models.CharField(blank=True, help_text='antares.apps.document.models.indexed_field.string_value_help', max_length=2000, null=True, verbose_name='antares.apps.document.models.indexed_field.string_value')),
                ('text_value', models.TextField(blank=True, help_text='antares.apps.document.models.indexed_field.text_value_help', null=True, verbose_name='antares.apps.document.models.indexed_field.text_value')),
                ('uuid_value', models.UUIDField(blank=True, help_text='antares.apps.document.models.indexed_field.uuid_value_help', null=True, verbose_name='antares.apps.document.models.indexed_field.uuid_value')),
                ('document', models.ForeignKey(db_column='document', help_text='antares.apps.document.models.indexed_field.document_help', on_delete=django.db.models.deletion.CASCADE, related_name='indexed_field_set', to='document.DocumentHeader', verbose_name='antares.apps.document.models.indexed_field.document')),
                ('form_definition', models.ForeignKey(db_column='form_definition', help_text='antares.apps.document.models.indexed_field.form_definition_help', on_delete=django.db.models.deletion.CASCADE, related_name='indexed_field_set', to='document.FormDefinition', verbose_name='antares.apps.document.models.indexed_field.form_definition')),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.indexed_field.table_name',
                'verbose_name_plural': 'antares.apps.document.models.indexed_field.table_name_plural',
                'db_table': 'doc_indexed_field',
            },
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='antares.apps.document.models.status_log.primary_key_help', primary_key=True, serialize=False, verbose_name='antares.apps.document.models.status_log.id')),
                ('status', enumfields.fields.EnumField(enum=DocumentStatusType, help_text='antares.apps.document.models.status_log.status_help', max_length=30, verbose_name='antares.apps.document.models.status_log.status')),
                ('status_date', models.DateTimeField(help_text='antares.apps.document.models.status_log.status_date_help', verbose_name='antares.apps.document.models.status_log.status_date')),
                ('user_id', models.UUIDField(blank=True, help_text='antares.apps.document.models.status_log.user_id_help', null=True, verbose_name='antares.apps.document.models.status_log.id')),
                ('document_id', models.UUIDField(help_text='antares.apps.document.models.status_log.document_id_help', verbose_name='antares.apps.document.models.status_log.document_id')),
            ],
            options={
                'verbose_name': 'antares.apps.document.models.status_log.table_name',
                'verbose_name_plural': 'antares.apps.document.models.status_log.table_name_plural',
                'db_table': 'doc_status_log',
            },
        ),
    ]
