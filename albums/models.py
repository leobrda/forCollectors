from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary.uploader


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
    image = CloudinaryField('image', folder='media/items', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.collection.name}"

@receiver(post_delete, sender=Item)
def delete_item_image(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)


@receiver(pre_save, sender=Item)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Item.objects.get(pk=instance.pk).image
    except Item.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file:
            cloudinary.uploader.destroy(old_file.public_id)