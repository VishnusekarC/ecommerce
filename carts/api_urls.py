from django.urls import path

from . import api_views

app_name = 'api-carts'

urlpatterns = [
    path('add-to-cart/', view=api_views.AddToCartAPIView.as_view(), name='add-to-cart'),
    path('remove-from-cart/', view=api_views.RemoveFromCartAPIView.as_view(),
         name='remove-from-cart'),
    path('get-my-cart/', view=api_views.GetMyCartAPIView.as_view(), name='get-my-cart'),
    path('select-delivery-address/', view=api_views.SelectAddressAPIView.as_view(),
         name='select-delivery-address')
]
