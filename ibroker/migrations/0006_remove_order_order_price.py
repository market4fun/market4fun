# Generated by Django 2.2.1 on 2019-06-22 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibroker', '0005_order_order_stock_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_price',
        ),
    ]