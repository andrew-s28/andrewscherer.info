from django.contrib import admin

from .models import ContactMe

# Register your models here.


@admin.register(ContactMe)
class ContactMeAdmin(admin.ModelAdmin):
    pass
