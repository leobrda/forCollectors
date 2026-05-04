from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Collection, Item
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


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk, collection__owner=request.user)
    collection = item.collection

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'albums/item_form.html', {'form': form, 'collection': collection, 'is_edit': True})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, collection__owner=request.user)
    collection = item.collection

    if request.method == 'POST':
        item.delete()
        return redirect('collection_detail', pk=collection.pk)

    return render(request, 'albums/item_confirm_delete.html', {'item': item})


@login_required
def dashboard(request):
    total_collections = request.user.collections.count()
    total_items = Item.objects.filter(collection__owner=request.user).count()
    recent_items = Item.objects.filter(collection__owner=request.user).order_by('-id')[:5]

    return render(request, 'albums/dashboard.html', {
        'total_collections': total_collections,
        'total_items': total_items,
        'recent_items': recent_items,
    })