# Generated by Django 2.2.9 on 2020-02-28 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20190629_1936'),
        ('core', '0004_auto_20200120_1817'),
        ('accounting', '0017_auto_20200228_2033'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='accountcharge',
            unique_together={('client', 'concept_type', 'period', 'account_type', 'charge_period', 'charge_type')},
        ),
    ]
