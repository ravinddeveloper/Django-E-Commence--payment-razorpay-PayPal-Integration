# Generated by Django 4.2.4 on 2023-11-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_cart_buy_alter_cart_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
