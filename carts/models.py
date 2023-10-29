import uuid

from accounts.models import CustomUserAddress
from django.db import models
from ecommerce import settings
from ecommerce.settings import MIN_ORD_VALUE, SHIPPING_PRICE, TAX_IN_PERCENTAGE
from products.models import Product
from utilities.models import TimestampedModel


class Cart(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=str(
        uuid.uuid4()), editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='carts', null=True, blank=True)
    address = models.ForeignKey(
        CustomUserAddress, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ec_carts'
        verbose_name_plural = 'Carts'

    def __str__(self) -> str:
        return str(self.id)

    @property
    def get_total(self):
        total = float(0)
        for item in self.cart_items.all():
            total += item.get_total
        return total

    @property
    def get_tax_amount(self):
        return float((TAX_IN_PERCENTAGE/100) * self.get_total)

    @property
    def get_total_with_tax(self):
        return float(self.get_total + self.get_tax_amount)

    @property
    def get_total_with_discount(self):
        return float(self.get_total_with_tax - float(self.discount)) if self.get_total_with_tax != 0 else 0

    @property
    def get_total_with_shipping(self):
        if self.get_total >= MIN_ORD_VALUE:
            return float(self.get_total_with_discount)
        return float(self.get_total_with_discount + SHIPPING_PRICE)

    @property
    def get_total_payable(self):
        return float(self.get_total_with_shipping)

    @property
    def is_shipping_price_applicable(self):
        return False if self.get_total >= MIN_ORD_VALUE else True

    @property
    def get_shipping_price(self):
        if self.get_total >= MIN_ORD_VALUE:
            return float(0)
        return float(SHIPPING_PRICE)


class CartItem(TimestampedModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'ec_cart_items'
        verbose_name_plural = 'CartItems'

    def __str__(self) -> str:
        return f'{self.id} - {self.cart.id}'

    @property
    def get_total(self):
        return float(self.product.price) * float(self.quantity)
