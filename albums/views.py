from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Collection
from .forms import CollectionForm


@login_required
def album_list(request):
    my_collections = Collection.objects.filter(owner=request.user)
    return render(request, 'albums/album_list.html', {'collections': my_collections})


@login_required
def collection_create(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.owner = request.user
            collection.save()
            return redirect('album_list')
    else:
        form = CollectionForm()

    return render(request, 'albums/collection_form.html', {'form': form})