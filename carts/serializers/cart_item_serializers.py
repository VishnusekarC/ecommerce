from rest_framework import serializers
from carts.models import CartItem
from products.serializers.product_serializer import ProductSerializer



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        product_serializer = ProductSerializer(instance.product, context={'request': request})
        data['product'] = product_serializer.data
        return data

