from django import forms
from .models import Spoj

choices = [(choice, spoj) for choice, spoj in enumerate(Spoj.objects.all())]


class AddFromCSVForm(forms.Form):
    file = forms.FileField(label="", required=True)
    spoj = forms.ChoiceField(label="Choose spoj", choices=choices, widget=forms.Select(attrs={"style": "height: 2.3612rem;"}))
