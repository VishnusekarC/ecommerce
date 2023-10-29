from django.urls import path

from . import api_views

app_name = 'api-products'

urlpatterns = [
    path('list-categories/', api_views.ListCategoriesAPIView.as_view(),
         name='list-categories'),
    path('list-collections/', api_views.ListCollectionsAPIView.as_view(),
         name='list-collections'),
    path('list-products/', api_views.ListProductsAPIView.as_view(),
         name='list-products'),
    path('list-products-by-category/<str:category>/',
         api_views.ListProductsByCategoryAPIView.as_view(), name='list-products-by-category'),
    path('list-products-by-collection/<str:collection>/',
        api_views.ListProductsByCollectionAPIView.as_view(), name='list-products-by-collection'),
    path('create-product/', api_views.CreateProductAPIView.as_view(), name='create-product'),
]
