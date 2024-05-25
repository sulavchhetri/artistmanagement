from django.urls import path

from .views import RegisterView, ViewArtists, ViewArtist, DeleteArtist, ModifyArtist

urlpatterns = [
    path('register/', RegisterView.as_view(), name='artist_register'),
    path('all/', ViewArtists.as_view(), name='artist_all'),
    path('<int:pk>/', ViewArtist.as_view(), name='artist_view'),
    path('delete/<int:pk>/', DeleteArtist.as_view(), name='artist_delete'),
    path('modify/<int:pk>/', ModifyArtist.as_view(), name='artist_modify')
]
