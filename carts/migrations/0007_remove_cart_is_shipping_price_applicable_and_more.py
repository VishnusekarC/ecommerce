# Generated by Django 4.2.6 on 2023-10-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_remove_cart_shipping_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_shipping_price_applicable',
        ),
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default='c49a2033-abfe-4992-a414-19dc01e33679', editable=False, primary_key=True, serialize=False),
        ),
    ]