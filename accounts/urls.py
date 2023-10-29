from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('activate/<uidb64>/<token>', views.ActivateView.as_view(), name='activate'),
    path('activate-success/', view=views.ActivateSuccessView.as_view(), name='activate-success'),
]





