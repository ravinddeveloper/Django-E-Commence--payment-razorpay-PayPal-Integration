# Generated by Django 4.2.4 on 2023-11-09 08:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_cart_added_date_cart_product_qty_cart_total_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='Added_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
    ]