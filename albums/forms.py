from django import forms
from .models import Collection, Item


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'year', 'description', 'image']