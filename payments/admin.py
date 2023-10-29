from django.contrib import admin
from .models import Payment, Transaction
from django import forms


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id','total', 'rzp_order_id', 'status')
    list_filter = ('status',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction)

