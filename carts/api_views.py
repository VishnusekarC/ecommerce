from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUserAddress

from .models import Cart, CartItem
from .serializers.cart_item_serializers import CartItemSerializer
from .serializers.get_cart_serializer import GetCartSerializer
from .serializers.remove_from_cart_serializers import RemoveFromCartSerializer
from .serializers.select_address_serializer import SelectAddressSerializer


class AddToCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data.get('product')
            quantity = serializer.validated_data.get('quantity')
            if not quantity:
                quantity = 1
            
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += quantity
                cart_item.save(update_fields=['quantity'])
                return Response('Quantity updated in cart', status=status.HTTP_201_CREATED)
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                return Response('Product Added to cart', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            
            # Find the cart item by product_id and the user's cart
            try:
                cart_item = CartItem.objects.get(cart__user=request.user, product__id=product_id)
            except CartItem.DoesNotExist:
                return Response("Product removed from the cart.", status=status.HTTP_404_NOT_FOUND)

            # Remove the cart item from the cart
            cart_item.delete()
            return Response("Product removed from the cart", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GetMyCartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = GetCartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response("User has no active cart, Add items to create cart.", status=status.HTTP_404_NOT_FOUND)
    


class SelectAddressAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SelectAddressSerializer(data=request.data)
        if serializer.is_valid():
            address_id = serializer.validated_data.get('address_id')
            try:
                custom_address = CustomUserAddress.objects.get(id=address_id)
            except CustomUserAddress.DoesNotExist:
                return Response('Cannot resolve address, Please choose right one!', status=status.HTTP_404_NOT_FOUND)
            
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                return Response('Cannot resolve cart', status=status.HTTP_404_NOT_FOUND)
            
            cart.address = custom_address
            cart.save(update_fields=['address'])
            return Response('Delivery address selected successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



