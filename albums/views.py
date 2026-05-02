from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Collection

@login_required
def album_list(request):
    my_collections = Collection.objects.filter(owner=request.user)
    return render(request, 'albums/album_list.html', {'collections': my_collections})