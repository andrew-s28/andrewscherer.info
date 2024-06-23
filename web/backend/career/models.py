from django.db import models

# Create your models here.


class Research(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    image = models.ImageField('research_image', upload_to='research/', null=True, blank=True)

    class Meta:
        verbose_name = 'Research'
        verbose_name_plural = 'Research'

    def __str__(self):
        return self.title


class Teaching(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    image = models.ImageField('teaching_image', upload_to='teaching/', null=True, blank=True)

    class Meta:
        verbose_name = 'Teaching'
        verbose_name_plural = 'Teaching'

    def __str__(self):
        return self.title


class Publications(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    image = models.ImageField('publication_image', upload_to='publication/', null=True, blank=True)

    class Meta:
        verbose_name = 'Publications'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return self.title


class Presentations(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    image = models.ImageField('presentation_image', upload_to='presentation/', null=True, blank=True)

    class Meta:
        verbose_name = 'Presentations'
        verbose_name_plural = 'Presentations'

    def __str__(self):
        return self.title


class CV(models.Model):
    cv = models.FileField(upload_to='cv/', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CV'
        verbose_name_plural = 'CV'

    @property
    def get_file(self):
        if self.cv and hasattr(self.cv, 'url'):
            return self.cv.url

    def __str__(self):
        return self.cv.name
