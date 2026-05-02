from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('new/', views.collection_create, name='collection_create'),
]