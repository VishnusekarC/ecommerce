from rest_framework import serializers


class RemoveCouponsSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    