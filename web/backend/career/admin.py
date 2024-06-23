from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Research, CV, Teaching, Publications, Presentations

# Register your models here.


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(Publications)
class PublicationsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(Presentations)
class PresentationsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    pass
