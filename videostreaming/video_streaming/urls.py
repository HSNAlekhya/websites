from django.urls import path
from .views import (
    HomeView,
    VideoListView,
    VideoPlayerView,
    AudioPlayerView,
    PlaylistView,
    VideoCreateView,
    VideoUpdateView,
    VideoDeleteView,
    remove_video,
    video_meta,
    proxy_stream,
    PlaylistCreateView,
    PlaylistUpdateView,
    PlaylistDeleteView,
    PlaylistDetailView,
    SearchView,
    file_list,
)

app_name = 'video_streaming'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('videos/', VideoListView.as_view(), name='video_list'),
    path('video/<int:pk>/', VideoPlayerView.as_view(), name='video_player'),
    path('video/<int:pk>/meta/', video_meta, name='video_meta'),
    path('video/<int:pk>/proxy/', proxy_stream, name='video_proxy'),
    path('video/create/', VideoCreateView.as_view(), name='video_create'),
    path('video/<int:pk>/edit/', VideoUpdateView.as_view(), name='video_edit'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
    path('video/<int:pk>/remove/', remove_video, name='video_remove'),
    path('audio/<int:pk>/', AudioPlayerView.as_view(), name='audio_player'),
    path('playlist/', PlaylistView.as_view(), name='playlist_list'),
    path('playlist/create/', PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/<int:pk>/edit/', PlaylistUpdateView.as_view(), name='playlist_edit'),
    path('playlist/<int:pk>/delete/', PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('search/', SearchView, name='search'),
    path('files/', file_list, name='file_list'),
]
