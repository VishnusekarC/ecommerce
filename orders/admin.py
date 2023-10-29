from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'grand_total', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)