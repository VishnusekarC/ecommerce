

from django.urls import path

from . import api_views

app_name = 'api-orders'

urlpatterns = [
    path('create-order/', view=api_views.CreateOrderAPIView.as_view(),
         name='create-order/'),
    path('my-pending-orders/', view=api_views.MyPendingOrdersAPIView.as_view(),
         name='my-pending-orders/'),
    path('my-processing-orders/', view=api_views.MyProcessingOrdersAPIView.as_view(),
         name='my-processing-orders/'),
    path('cancel-order/<int:order_id>/',
         view=api_views.CancelOrderAPIView.as_view(), name='cancel-order'),
    path('my-cancelled-orders/', view=api_views.MyCancelledOrdersAPIView.as_view(),
         name='my-cancelled-orders'),

]
