# Generated by Django 4.2.4 on 2023-11-09 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_remove_cart_added_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cart',
        ),
    ]