from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationView, LogoutView, LoginView, UserDetailView, UserListView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
    path('user-list/', UserListView.as_view(), name='user-list'),
]