# Generated by Django 3.1.6 on 2021-02-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maze', '0002_gamestart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestart',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
