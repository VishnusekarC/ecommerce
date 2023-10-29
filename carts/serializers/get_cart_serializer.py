from rest_framework import serializers
from carts.models import Cart
from .cart_item_serializers import CartItemSerializer




class GetCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ('created_at', 'updated_at')
        # depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Cart Items
        cart_items = instance.cart_items.all()
        cart_item_serializer = CartItemSerializer(cart_items, many=True)
        data['cart_items'] = cart_item_serializer.data
      
        data['total'] = instance.get_total
        data['tax'] = instance.get_tax_amount
        data['total_with_tax'] = instance.get_total_with_tax
        data['total_with_discount'] = instance.get_total_with_discount
        data['total_with_shipping'] = instance.get_total_with_shipping
        data['total_payable'] = instance.get_total_payable
        data['is_shipping_price_applicable'] = instance.is_shipping_price_applicable
        data['shipping_price'] = instance.get_shipping_price
        return data



        