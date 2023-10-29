
from rest_framework import serializers


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()