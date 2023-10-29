from django.urls import path
from . import api_views

app_name = 'api-coupons'

urlpatterns = [
    path('get-coupons/', view=api_views.GetAvailableCouponAPIView.as_view(), name='get-coupons'),
    path('apply-coupon/', view=api_views.ApplyCouponAPIView.as_view(), name='apply-coupon'),
    path('remove-coupon/', view=api_views.RemoveCouponAPIView.as_view(), name='remove-coupon'),
    path('create-coupon/', view=api_views.CreateCouponAPIView.as_view(), name='create-coupon')
]


