from django import forms
from .models import SocialSearch

class SocialSearchModelForm(forms.ModelForm):
    class Meta:
        model = SocialSearch
        exclude = ("user",)
