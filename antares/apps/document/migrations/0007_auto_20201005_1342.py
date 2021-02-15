# Generated by Django 3.1.2 on 2020-10-05 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0006_auto_20200324_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='data_type',
            field=models.CharField(choices=[('String', 'String'), ('Text', 'Text'), ('Date', 'Date'), ('Datetime', 'Date time'), ('Integer', 'Integer'), ('Float', 'Float'), ('UUID', 'UUID'), ('Boolean', 'Boolean'), ('User', 'User'), ('client', 'Client'), ('document', 'Document'), ('Money', 'Money')], help_text='antares.apps.document.models.document_field.data_type_help', max_length=30, verbose_name='antares.apps.document.models.document_field.data_type'),
        ),
        migrations.AlterField(
            model_name='documenttablecontent',
            name='data_type',
            field=models.CharField(blank=True, choices=[('String', 'String'), ('Text', 'Text'), ('Date', 'Date'), ('Datetime', 'Date time'), ('Integer', 'Integer'), ('Float', 'Float'), ('UUID', 'UUID'), ('Boolean', 'Boolean'), ('User', 'User'), ('client', 'Client'), ('document', 'Document'), ('Money', 'Money')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='indexedfield',
            name='data_type',
            field=models.CharField(choices=[('String', 'String'), ('Text', 'Text'), ('Date', 'Date'), ('Datetime', 'Date time'), ('Integer', 'Integer'), ('Float', 'Float'), ('UUID', 'UUID'), ('Boolean', 'Boolean'), ('User', 'User'), ('client', 'Client'), ('document', 'Document'), ('Money', 'Money')], help_text='antares.apps.document.models.indexed_field.data_type_help', max_length=30, verbose_name='antares.apps.document.models.indexed_field.data_type'),
        ),
    ]