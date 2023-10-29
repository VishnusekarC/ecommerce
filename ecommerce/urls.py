"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ecommerce import settings
from payments.views import RazorPayWebHookView

admin.site.site_title = 'Nuno Shop'
admin.site.site_header = 'Nuno Shop'
admin.site.index_title = 'Nuno Shop'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/capture/', RazorPayWebHookView.as_view(), name='payment-capture'),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/accounts/', include('accounts.api_urls', namespace='api-accounts')),
    path('api/products/', include('products.api_urls', namespace='api-products')),
    path('api/carts/', include('carts.api_urls', namespace='api-carts')),
    path('api/coupons/', include('coupon.api_urls', namespace='api-coupons')),
    path('api/orders/', include('orders.api_urls', namespace='api-orders')),

]

# URL patterns for serving media files during development
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

