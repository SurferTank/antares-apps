# Generated by Django 3.0.4 on 2020-03-07 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0021_auto_20200306_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdocument',
            name='status',
            field=models.CharField(choices=[('Pending', 'antares.apps.accounting.constants.AccountDocumentStatusType.PENDING'), ('Processed', 'antares.apps.accounting.constants.AccountDocumentStatusType.PROCESSED'), ('With Errors', 'antares.apps.accounting.constants.AccountDocumentStatusType.WITH_ERRORS'), ('On hold', 'antares.apps.accounting.constants.AccountDocumentStatusType.ON_HOLD'), ('Cancelled', 'antares.apps.accounting.constants.AccountDocumentStatusType.CANCELLED')], max_length=30),
        ),
        migrations.AlterField(
            model_name='accountrule',
            name='value_affected',
            field=models.CharField(choices=[('Principal', 'Principal'), ('Interest', 'Interest'), ('Penalties', 'Penalties')], max_length=20),
        ),
        migrations.AlterField(
            model_name='interestdefinition',
            name='periodicity',
            field=models.CharField(choices=[('Year', 'Year'), ('Month', 'Month'), ('Day', 'Day'), ('Hour', 'Hour'), ('Minute', 'Minute'), ('Second', 'Second')], default='Month', max_length=10),
        ),
        migrations.AlterField(
            model_name='penaltydefinition',
            name='periodicity',
            field=models.CharField(choices=[('Year', 'Year'), ('Month', 'Month'), ('Day', 'Day'), ('Hour', 'Hour'), ('Minute', 'Minute'), ('Second', 'Second')], default='Month', max_length=10),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='effect',
            field=models.CharField(choices=[('Debit', 'Debit'), ('Credit', 'Credit')], max_length=6),
        ),
    ]