# Generated by Django 4.2.6 on 2023-10-25 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0006_alter_order_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=9)),
                ('rzp_order_id', models.CharField(max_length=40)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('AUTHORIZED', 'AUTHORIZED'), ('CAPTURED', 'CAPTURED'), ('REFUNDED', 'REFUNDED'), ('FAILED', 'FAILED')], default='CREATED', max_length=20)),
                ('raw_data', models.JSONField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order')),
            ],
            options={
                'db_table': 'ec_payments',
            },
        ),
    ]
