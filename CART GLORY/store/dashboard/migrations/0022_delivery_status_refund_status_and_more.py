# Generated by Django 4.2.4 on 2023-11-24 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_address_hide_cart_address_order_delivery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_status',
            name='refund_status',
            field=models.CharField(choices=[('initiated', 'initiated'), ('completed', 'completed'), ('none', 'none')], default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='delivery_status',
            name='status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('Shipped', 'Shipped'), ('arrived', 'arrived'), ('delivered', 'delivered'), ('OFD', 'OFD'), ('Rejected', 'Rejected'), ('Returned', 'Returned'), ('canceled', 'canceled')], default='Processing', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='dashboard.cart'),
        ),
    ]