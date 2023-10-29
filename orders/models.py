from django.db import models
from utilities.models import TimestampedModel
from products.models import Product
from ecommerce import settings
from accounts.models import CustomUserAddress


class Order(TimestampedModel):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('PROCESSING', 'PROCESSING'),
        ('SHIPPED', 'SHIPPED'),
        ('RETURNED', 'RETURNED'),
        ('CANCELLED', 'CANCELLED'),
        ('DELIVERED', 'DELIVERED')
    )

    status = models.CharField(max_length=25, choices=ORDER_STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='orders')
    address = models.ForeignKey(
        CustomUserAddress, on_delete=models.CASCADE)
    shipping_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=20, null=True, blank=True)
    cart_id = models.UUIDField()
    total = models.DecimalField(max_digits=9, decimal_places=2)
    tax = models.DecimalField(max_digits=9, decimal_places=2)
    grand_total = models.DecimalField(max_digits=9, decimal_places=2)
    processed_on = models.DateField(null=True, blank=True)
    is_payment_successful = models.BooleanField(default=False)
    is_captured = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)
    is_cod = models.BooleanField(default=False)

    class Meta:
        db_table = 'ec_orders'
        verbose_name_plural = 'Orders'
    
    def __str__(self) -> str:
        return f'#{self.id}'
    
    @property
    def legacy_order_id(self):
        return int(100000000 + self.id)



class OrderItem(TimestampedModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'ec_order_items'
        verbose_name_plural = 'Order Items'
    
    def __str__(self) -> str:
        return f'{self.id} - {self.order.id}'

