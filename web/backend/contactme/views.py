from django.shortcuts import render
from django.utils import timezone
from django.views.generic import FormView
from django.shortcuts import reverse
from django.core.mail import send_mail, backends
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect

from .models import ContactMe
from .forms import ContactMeForm

# Create your views here.


def contact_success_view(request):
    return render(request, 'contactme/success.html', {"message": "Thank you for your submission. I will get back to you as soon as possible."})


class ContactMeView(FormView):
    form_class = ContactMeForm
    template_name = "contactme/contactme.html"
    context_object_name = "contactme"

    def get_success_url(self):
        return reverse("contactme:success")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        comments = form.cleaned_data.get("comments")
        if comments:
            print("Spam detected")
            return HttpResponseRedirect(reverse('contactme:success'))

        full_message = f"""
            Received message below from {email}
            Name: {name}
            Re: {subject}
            _______________________________________

            {message}
            """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return HttpResponseRedirect(reverse('contactme:success'))
