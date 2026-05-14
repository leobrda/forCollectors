from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
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
            messages.success(request, f"Coleção '{collection.name}' criada com sucesso!")
            return redirect('album_list')
    else:
        form = CollectionForm()

    return render(request, 'albums/collection_form.html', {'form': form})


@login_required
def collection_update(request, pk):
    collection = get_object_or_404(Collection, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, f"Coleção '{collection.name}' atualizada!")
            return redirect('album_list')
    else:
        form = CollectionForm(instance=collection)
    return render(request, 'albums/collection_form.html', {'form': form})


@login_required
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if not collection.is_public and collection.owner != request.user:
        messages.error(request, "Esta coleção é privada e você não tem permissão para visualizá-la.")
        return redirect('album_list')

    items = collection.items.all()

    search_query = request.GET.get('search')
    if search_query:
        filters = Q(title__icontains=search_query) | Q(description__icontains=search_query)

        if search_query.isdigit():
            filters |= Q(year=int(search_query))

        items = items.filter(filters)

    return render(request, 'albums/collection_detail.html', {'collection': collection, 'items': items, 'search_query': search_query})


@login_required
def item_create(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)

    if collection.owner != request.user:
        messages.error(request, "Ação negada: Você só pode adicionar itens às suas próprias coleções.")
        return redirect('collection_detail', pk=collection.pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.collection = collection
            item.save()
            messages.success(request, f"O item '{item.title}' foi adicionado à coleção '{collection.name}'!")
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
            messages.success(request, f"As alterações no item '{item.title}' foram salvas com sucesso!")
            return redirect('collection_detail', pk=collection.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'albums/item_form.html', {'form': form, 'collection': collection, 'is_edit': True})


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, collection__owner=request.user)
    collection = item.collection

    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f"O item '{title}' foi deletado com sucesso!")
        return redirect('collection_detail', pk=item.collection.pk)

    return render(request, 'albums/item_confirm_delete.html', {'item': item})


@login_required
def dashboard(request):
    total_collections = request.user.collections.count()
    total_items = Item.objects.filter(collection__owner=request.user).count()
    recent_items = Item.objects.filter(collection__owner=request.user).order_by('-id')[:5]

    collections = request.user.collections.annotate(num_items=Count('items'))
    chart_labels = [c.name for c in collections]
    chart_data = [c.num_items for c in collections]

    return render(request, 'albums/dashboard.html', {
        'total_collections': total_collections,
        'total_items': total_items,
        'recent_items': recent_items,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })


@login_required
def item_list(request):
    search_query = request.GET.get('search')
    items = Item.objects.filter(collection__owner=request.user)

    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'albums/item_list.html', {
        'items': items,
        'search_query': search_query
    })


@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        collection.delete()
        messages.success(request, f'A coleção "{collection.name}" e todos os seus itens foram excluídos!')
        return redirect('album_list')
    
    return render(request, 'albums/collection_confirm_delete.html', {'object': collection})


@login_required
def global_search(request):
    query = request.GET.get('q')
    items = Item.objects.filter(
        Q(collection__is_public=True) | Q(collection__owner=request.user)
    )

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(collection__name__icontains=query) |
            Q(collection__owner__username__icontains=query)
        ).distinct()

    return render(request, 'albums/global_search_results.html', {'items': items, 'query': query})


@login_required
def explore(request):
    items = Item.objects.filter(collection__is_public=True).exclude(collection__owner=request.user).order_by('-id')
    return render(request, 'albums/explore.html', {'items': items})