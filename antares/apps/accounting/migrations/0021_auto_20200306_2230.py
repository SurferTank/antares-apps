# Generated by Django 3.0.4 on 2020-03-07 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0020_auto_20200229_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountbalance',
            name='balance_status',
            field=models.CharField(choices=[('Debit', 'antares.apps.accounting.constants.BalanceStatusType.DEBIT'), ('Credit', 'antares.apps.accounting.constants.BalanceStatusType.CREDIT'), ('Balanced', 'antares.apps.accounting.constants.BalanceStatusType.BALANCED')], default='Balanced', max_length=10),
        ),
    ]
