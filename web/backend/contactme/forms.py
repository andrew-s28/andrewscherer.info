from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import ContactMe


class ContactMeForm(forms.ModelForm):
    template_name = "contactme/contactme_form.html"
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="")
    comments = forms.CharField(widget=forms.Textarea, required=False, label="comments")

    class Meta:
        model = ContactMe
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }
