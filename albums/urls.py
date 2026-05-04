from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('new/', views.collection_create, name='collection_create'),
    path('collection/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('collection/<int:collection_pk>/add-item/', views.item_create, name='item_create'),
]