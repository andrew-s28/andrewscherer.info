from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE


from .models import BlogPost, UploadedImages

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'pub_date', 'tags', 'body', 'image',)
        }),
    )

    class Media:
        js = ('tinyinject.js',)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogPost, BlogAdmin)
admin.site.register(UploadedImages, ImageAdmin)
