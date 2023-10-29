from django.urls import path
from . import api_views

app_name = 'api-accounts'

urlpatterns = [
    # Authentication
    path('register/', view=api_views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', view=api_views.LoginUserAPIView.as_view(), name='login'),

    # Users
    path('create-user-detail/', view=api_views.CreateUserDetailAPIView.as_view(),
         name='create-user-detail'),
    path('get-my-detail/',
         api_views.RetrieveCustomUserDetailAPIView.as_view(), name='get-my-detail'),

   # User Address:
   path('add-address/', view=api_views.CreateUserAddressAPIView.as_view(), name='add-address'),
   path('get-my-addresses/', view=api_views.GetMyAddressesAPIView.as_view(), name='get-my-addresses')
]
