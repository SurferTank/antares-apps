# Generated by Django 2.2.9 on 2020-02-29 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0019_auto_20200228_2056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='penaltydefinition',
            old_name='fixed_rate',
            new_name='fixed_amount',
        ),
        migrations.RenameField(
            model_name='penaltydefinition',
            old_name='fixed_rate_currency',
            new_name='fixed_amount_currency',
        ),
    ]
