# Generated by Django 4.2.7 on 2023-12-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallchop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_type',
            field=models.TimeField(choices=[('AM', 'AM'), ('PM', 'PM')], default='AM'),
        ),
    ]
