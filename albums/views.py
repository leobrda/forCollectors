from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Collection
from .forms import CollectionForm, ItemForm


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


@login_required
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk, owner=request.user)
    items = collection.items.all()

    return render(request, 'albums/collection_detail.html', {'collection': collection, 'items': items})


@login_required
def item_create(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk, owner=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.collection = collection
            item.save()
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = ItemForm()

    return render(request, 'albums/item_form.html', {'form': form, 'collection': collection})

