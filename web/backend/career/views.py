from django.shortcuts import render

from django.utils import timezone

from .models import Research, CV, Teaching, Publications, Presentations

# Create your views here.


def career_view(request):
    cv = CV.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    research = Research.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    teaching = Teaching.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    publications = Publications.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    presentations = Presentations.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').first()
    context = {
        'cv': cv,
        'research': research,
        'teaching': teaching,
        'publications': publications,
        'presentations': presentations,
    }
    return render(request, 'career/career.html', context)
