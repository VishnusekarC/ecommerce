from django.db import models
from utilities.models import TimestampedModel
from orders.models import Order


class Payment(TimestampedModel):
    PAYMENT_STATUS_CHOICES = (
        ('CREATED', 'CREATED'),
        ('AUTHORIZED', 'AUTHORIZED'),
        ('CAPTURED', 'CAPTURED'),
        ('REFUNDED', 'REFUNDED'),
        ('FAILED', 'FAILED'),
    ) 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    total = models.DecimalField(max_digits=9, decimal_places=2)
    rzp_order_id = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='CREATED')
    raw_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'ec_payments'

    def __str__(self) -> str:
        return f'{self.id}'


class Transaction(TimestampedModel):
    raw_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'ec_transactions'

    def __str__(self) -> str:
        return f'#{self.id}'

    
