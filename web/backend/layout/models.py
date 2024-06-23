from django.db import models

# Create your models here.


class Homepage(models.Model):
    site_name = models.CharField(max_length=50)
    welcome_message = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.site_name


class Navbar(models.Model):
    page = models.CharField(max_length=50)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.page
