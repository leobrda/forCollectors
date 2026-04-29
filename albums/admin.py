from django.contrib import admin
from .models import Collection, Item

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'collection', 'year')
    list_filter = ('collection', 'year')