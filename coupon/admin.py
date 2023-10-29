from django.contrib import admin
from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'coupon_code', 'min_ord_value', 'discount_amount','expiry_date','is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)

admin.site.register(Coupon, CouponAdmin)