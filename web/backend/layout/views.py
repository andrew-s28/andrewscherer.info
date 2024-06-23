from django.shortcuts import render
from .models import Homepage

# Create your views here.


def index(request):
    homepage = Homepage.objects.get(id=1)
    return render(request, 'layout/homepage.html', {'homepage': homepage})
