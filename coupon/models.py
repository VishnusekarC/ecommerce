from django.db import models
from utilities.models import TimestampedModel


class Coupon(TimestampedModel):
    name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    min_ord_value = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Minimum Order Value')
    discount_amount = models.DecimalField(max_digits=7, decimal_places=2)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ec_coupons'
        verbose_name_plural = 'Coupons'

    def __str__(self) -> str:
        return self.coupon_code
    

