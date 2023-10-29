from django.contrib import admin
from .models import Cart, CartItem



class CartItemInline(admin.StackedInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'cart_items', 'get_total')
    inlines = [CartItemInline,]

    def cart_items(self, obj):
        return obj.cart_items.count()

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','user')

    def user(self, obj):
        return obj.cart.user.email

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
