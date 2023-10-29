from rest_framework import generics
from rest_framework.permissions import AllowAny

from products.serializers.category_serializer import CategorySerializer
from products.serializers.collection_serializer import CollectionSerializer
from products.serializers.product_serializer import ProductSerializer, CreateProductSerializer

from .models import Category, Collection, Product
from accounts.api_permissions import IsManager
from rest_framework.permissions import IsAuthenticated



class CreateProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = (IsAuthenticated, IsManager)




class ListCategoriesAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class ListCollectionsAPIView(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class ListProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True)


class ListProductsByCategoryAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category_slug = self.kwargs['category']
        return self.queryset.filter(is_active=True, categories__slug=category_slug)


class ListProductsByCollectionAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        collection_slug = self.kwargs['collection']
        return self.queryset.filter(is_active=True, collections__slug=collection_slug)
