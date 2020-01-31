# Generated by Django 2.2.9 on 2020-01-31 12:56

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_auto_20190629_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='interest_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='penalties_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='principal_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='total_amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='glbalance',
            name='credit_balance',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='glbalance',
            name='debit_balance',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='gltransaction',
            name='credit_balance',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='gltransaction',
            name='debit_balance',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='USD', editable=False, max_digits=10),
        ),
    ]
