from rest_framework import serializers

class ApplyCouponsSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    coupon_code = serializers.CharField()
