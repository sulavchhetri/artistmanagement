from django.urls import path

from .views import (RegisterView,
                    ViewArtists,
                    ViewArtist,
                    DeleteArtist,
                    ModifyArtist,
                    ViewSongs,
                    ViewSong,
                    AddSong,
                    DeleteSong,
                    ModifySong)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='artist_register'),
    path('all/', ViewArtists.as_view(), name='artist_all'),
    path('<int:pk>/', ViewArtist.as_view(), name='artist_view'),
    path('delete/<int:pk>/', DeleteArtist.as_view(), name='artist_delete'),
    path('modify/<int:pk>/', ModifyArtist.as_view(), name='artist_modify'),
    path('<int:pk>/songs/', ViewSongs.as_view(), name='view_songs'),
    path('<int:pk>/songs/<int:song_id>/', ViewSong.as_view(), name='view_song'),
    path('<int:pk>/songs/add/', AddSong.as_view(), name='add_song'),
    path('<int:pk>/songs/<int:song_id>/delete/', DeleteSong.as_view(), name='delete_song'),
    path('<int:pk>/songs/<int:song_id>/modify/', ModifySong.as_view(), name='modify_song')
]
