# Generated by Django 4.2.4 on 2023-11-09 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_cart_added_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='Added_date',
        ),
    ]
