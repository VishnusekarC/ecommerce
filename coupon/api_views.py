from carts.models import Cart
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.api_permissions import IsManager

from .models import Coupon
from .serializers.apply_coupon_serializer import ApplyCouponsSerializer
from .serializers.get_coupons_serializer import GetCouponsSerializer, CreateCouponSerializer
from .serializers.remove_coupon_serializer import RemoveCouponsSerializer
from accounts.utils import check_is_manager


class CreateCouponAPIView(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = CreateCouponSerializer


class GetAvailableCouponAPIView(generics.ListAPIView):
    queryset = Coupon.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetCouponsSerializer

    def get_queryset(self):
        if check_is_manager(user=self.request.user):
            return self.queryset.all()
        return self.queryset.filter(is_active=True, expiry_date__gte=timezone.now().date())


class ApplyCouponAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = ApplyCouponsSerializer(data=request.data)
        if serializer.is_valid():
            cart_id = serializer.validated_data.get('cart_id')
            coupon_code = serializer.validated_data.get('coupon_code')
            try:
                cart = Cart.objects.get(id=cart_id, user=request.user)
            except Cart.DoesNotExist:
                return Response('Cannot resolve cart for user.', status=status.HTTP_200_OK)

            try:
                coupon = Coupon.objects.get(
                    coupon_code=coupon_code, is_active=True, expiry_date__gte=timezone.now().date())
            except Coupon.DoesNotExist:
                return Response('Coupon invalid!', status=status.HTTP_200_OK)

            # Check if the coupon is already used by the user (is pending)

            if cart.get_total >= coupon.min_ord_value:
                cart.coupon_code = coupon.coupon_code
                cart.discount = coupon.discount_amount
                cart.save(update_fields=['coupon_code', 'discount'])
                return Response('Enjoy! Coupon Applied Successfully.', status=status.HTTP_200_OK)
            return Response(f'Your cart total is less than {coupon.min_ord_value}.', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveCouponAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = RemoveCouponsSerializer(data=request.data)
        
        if serializer.is_valid():
            cart_id = serializer.validated_data.get('cart_id')
            try:
                cart = Cart.objects.get(id=cart_id, user=request.user)
            except Cart.DoesNotExist:
                return Response('Cannot resolve cart for user.', status=status.HTTP_200_OK)
            if cart.coupon_code:
                cart.coupon_code = None
                cart.discount = 0
                cart.save(update_fields=['coupon_code', 'discount'])
                return Response('Coupon Removed Successfully!', status=status.HTTP_200_OK)
            return Response('No coupon to remove!', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
