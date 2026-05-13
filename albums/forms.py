from django import forms
from .models import Collection, Item


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description', 'is_public']
        widgets = {
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'year', 'description', 'image']