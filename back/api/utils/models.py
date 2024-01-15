from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def dynamic_upload_to(instance, filename):
    # Generate a dynamic upload path based on the related model's name
    return f'uploads/{instance.content_type}/{timezone.now().strftime("%Y/%m/%d")}/{filename}'


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    image = models.ImageField(upload_to=dynamic_upload_to)

    def __str__(self):
        return self.image.url
