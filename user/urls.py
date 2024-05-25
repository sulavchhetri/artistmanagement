from django.urls import path
from .views import RegisterView, LoginView, logout_view, DashboardView, ViewUser, ViewUsers

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('user/login/', LoginView.as_view(), name='user_login'),
    path('user/register/', RegisterView.as_view(), name='user_register'),
    path('user/logout/', logout_view, name='user_logout'),
    path('user/all/', ViewUsers.as_view(), name='user_all'),
    path('user/<int:pk>/', ViewUser.as_view(), name='user_view')
]
