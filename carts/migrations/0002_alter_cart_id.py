# Generated by Django 4.2.6 on 2023-10-14 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default='9ace9cc7-7', editable=False, primary_key=True, serialize=False),
        ),
    ]