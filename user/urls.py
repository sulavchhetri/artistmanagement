from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('user/login/', LoginView.as_view(), name='user_login'),
    path('user/register/', RegisterView.as_view(), name='user_register'),
    path('user/logout/', LogoutView.as_view(), name='user_logout')
]
