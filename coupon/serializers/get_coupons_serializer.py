from rest_framework import serializers
from coupon.models import Coupon



class CreateCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        exclude = ('created_at', 'updated_at')


class GetCouponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('id', 'coupon_code', 'description')

    