# Generated by Django 4.2.4 on 2023-11-09 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_cart_added_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]