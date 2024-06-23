from django.shortcuts import render
from django.utils import timezone

from .models import AboutMe

# Create your views here.


def about_me_view(request):
    aboutme = AboutMe.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    return render(request, 'aboutme/aboutme.html', {'aboutme': aboutme})
