from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import AboutMe

# Register your models here.


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
