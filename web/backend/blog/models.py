from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.timezone import now
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from taggit.managers import TaggableManager

import os

# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField(default=now)
    image = models.ImageField('picture_lead', upload_to='blog/', null=True, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    slug = AutoSlugField(populate_from=('title',), unique=True, max_length=50)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    @property
    def date_formatted(self):
        return self.pub_date.strftime('%B %d, %Y')

    @property
    def date_slug(self):
        return self.pub_date.strftime('%Y-%m')


class UploadedImages(models.Model):
    image = models.ImageField(upload_to='tinymce/', null=True, blank=True)

    class Meta:
        verbose_name = 'Uploaded image'
        verbose_name_plural = 'Uploaded images'

    @property
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def __str__(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return 'No image'


@receiver(post_delete, sender=UploadedImages)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if os.path.exists(instance.image.path):
        os.remove(instance.image.path)
    instance.image.delete(False)
