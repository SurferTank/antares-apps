# Generated by Django 2.2.9 on 2020-02-10 16:51

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0014_auto_20200210_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='penaltydefinition',
            name='recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='interestdefinition',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='interestdefinition',
            name='rate',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='penaltydefinition',
            name='fixed_rate',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=2, default_currency='USD', max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='penaltydefinition',
            name='rate',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
