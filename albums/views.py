from django.shortcuts import render
from .models import Collection

def album_list(request):
    return render(request, 'albums/album_list.html')