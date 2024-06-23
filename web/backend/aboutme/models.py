from django.db import models

# Create your models here.


class AboutMe(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    image = models.ImageField('selfie', upload_to='aboutme/', null=True, blank=True)

    def __str__(self):
        return self.title
