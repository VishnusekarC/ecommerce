from carts.models import Cart
from django.db import transaction
from payments.serializers.payment_serializer import PaymentSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers.order_serializer import (CreateOrderSerializer,
                                           GenericOrderSerializer)
from .utils import create_order, create_payment_for_order


class CreateOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            cart_id = serializer.validated_data.get('cart_id')
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                return Response('Cannot resolve cart', status=status.HTTP_404_NOT_FOUND)
            if not cart.address:
                return Response('Must provide delivery address!', status=status.HTTP_404_NOT_FOUND)
            order = create_order(cart, user=request.user)
            cart.delete()
            payment = create_payment_for_order(order)
            payment_serializer = PaymentSerializer(payment)
            data = {
                'message': 'Order Created Successfully!',
                'payment': payment_serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelOrderAPIView(APIView):
    
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'CANCELLED':
             return Response({"detail": "Order already cancelled"}, status=status.HTTP_409_CONFLICT)
        if order.status == 'PENDING' or order.status == 'PROCESSING' or order.status == 'SHIPPED':
            order.status = 'CANCELLED'
            order.save(update_fields=['status'])

        # Serialize and return the updated order
        serializer = GenericOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MyCancelledOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GenericOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, status='CANCELLED')
        


class MyProcessingOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GenericOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, status='PROCESSING')
        


class MyPendingOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = GenericOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, status='PENDING')

