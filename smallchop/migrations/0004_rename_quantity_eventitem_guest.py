# Generated by Django 4.2.7 on 2023-12-13 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smallchop', '0003_alter_event_time_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventitem',
            old_name='quantity',
            new_name='guest',
        ),
    ]
