from django.contrib import admin
from .models import Homepage, Navbar

# Register your models here.


@admin.register(Homepage)
class HomepageAdmin(admin.ModelAdmin):
    pass


@admin.register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    pass
