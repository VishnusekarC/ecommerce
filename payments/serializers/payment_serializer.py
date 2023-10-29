from rest_framework import serializers
from payments.models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = ('created_at', 'updated_at')