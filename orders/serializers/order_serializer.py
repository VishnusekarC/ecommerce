from rest_framework import serializers
from orders.models import Order


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    

class GenericOrderSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        exclude = ('created_at', 'updated_at', 'id')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['order_id'] = instance.legacy_order_id
        return data