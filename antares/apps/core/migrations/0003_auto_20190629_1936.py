# Generated by Django 2.2.2 on 2019-06-29 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180624_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concepttype',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='concepttype',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]