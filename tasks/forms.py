from django import forms
from .models import Spoj
from django.core.validators import FileExtensionValidator

choices = [(choice, spoj) for choice, spoj in enumerate(Spoj.objects.all())]


class AddFromCSVForm(forms.Form):
    file = forms.FileField(label="", allow_empty_file=False)
    spoj = forms.ChoiceField(label="Choose spoj", choices=choices, widget=forms.Select(attrs={"style": "height: "
                                                                                                       "2.3612rem;"}))

    # From DOCS: Don’t rely on validation of the file extension to determine a file’s type.
    # Files can be renamed to have any extension no matter what data they contain.
    # So it's just for preventing human error
    file.validators.append(FileExtensionValidator(allowed_extensions=['csv'], message="File must have .csv extension"))
