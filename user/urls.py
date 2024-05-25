from django.urls import path
from .views import RegisterView, LoginView, logout_view, DashboardView, ViewUser, ViewUsers, DeleteUser, ModifyUser

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('user/login/', LoginView.as_view(), name='user_login'),
    path('user/register/', RegisterView.as_view(), name='user_register'),
    path('user/logout/', logout_view, name='user_logout'),
    path('user/<int:pk>/', ViewUser.as_view(), name='user_view'),
    path('all/', ViewUsers.as_view(), name='user_all'),
    path('user/delete/<int:pk>/', DeleteUser.as_view(), name='user_delete'),
    path('user/modify/<int:pk>/', ModifyUser.as_view(), name='user_modify')
]
