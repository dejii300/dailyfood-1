# Generated by Django 4.2.7 on 2023-12-20 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smallchop', '0013_remove_delivery_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shippingaddress',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smallchop.shippingaddress'),
        ),
    ]
