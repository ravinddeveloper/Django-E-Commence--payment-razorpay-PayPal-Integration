# Generated by Django 4.2.4 on 2023-11-14 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_cart_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='buy',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='dashboard.product'),
        ),
    ]