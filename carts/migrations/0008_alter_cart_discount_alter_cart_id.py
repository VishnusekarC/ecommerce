# Generated by Django 4.2.6 on 2023-10-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_remove_cart_is_shipping_price_applicable_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default='e98432fc-3d68-4bde-acbb-720ab471efa4', editable=False, primary_key=True, serialize=False),
        ),
    ]
