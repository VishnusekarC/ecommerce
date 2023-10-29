from rest_framework import serializers


class SelectAddressSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()