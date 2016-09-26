from django import forms
from .models import SocialSearch

class SocialSearchModelForm(forms.ModelForm):
    class Meta:
        model = SocialSearch
        exclude = ("user",)

class CSVExportForm(forms.Form):
    email_address = forms.EmailField(u"Email Address", required=True)

