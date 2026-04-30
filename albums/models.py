from django.db import models
from django.contrib.auth.models import User


class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.owner.username})'


class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.collection.name}"