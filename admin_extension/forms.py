from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.db import connection
from django.db.models import Model
import re

from tasks.models import Task, Spoj
from typing import List, Type


def get_choices():
    choices = []
    try:
        choices = [(choice, spoj) for choice, spoj in enumerate(Spoj.objects.iterator())]
    except:
        pass

    return choices


can_be_null = ["url", "solution_url"]
unwanted_in_tasks = ["id", "spoj", "user_tasks"]
model_fields = [
    f.name for f in Task._meta.get_fields() if f.name not in unwanted_in_tasks
]

split_pattern = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')


def check_same_strings(list1: List[str], list2: List[str]) -> bool:
    set1 = set(list1)
    set2 = set(list2)

    return set1 == set2


# Checks whether a certain string can be converted to a field of certain name contained in a certain Model
def is_valid_for_field(to_check: str, model: Type[Model], field_name: str) -> bool:
    field = model._meta.get_field(field_name)
    try:
        field.clean(to_check, None)
        return True
    except ValidationError:
        return False


def validate_csv(file: InMemoryUploadedFile) -> None:
    lines = file.readlines()
    if len(lines) <= 0:
        raise ValidationError("File cannot be empty!")

    csv_fields = re.split(split_pattern, lines[0].decode().strip())

    if not check_same_strings(csv_fields, model_fields):
        raise ValidationError(f"Incorrect headers! Expected: {model_fields} got: {csv_fields}")
    for index, line in enumerate(lines[1:]):
        fields = re.split(split_pattern, line.decode().replace("\r\n", ""))
        if len(fields) != len(csv_fields):
            raise ValidationError(
                f"Incorrect line length at line {index + 2}, expected: {len(csv_fields)}, got: {len(fields)}, {fields}")

        # Checks argument types
        for idx, field in enumerate(fields):
            if (field == "" and field in can_be_null) or not is_valid_for_field(
                    field, Task, csv_fields[idx]
            ):
                raise ValidationError(
                    f"Incorrect value at line {index + 2}, field {idx + 1}"
                )


class AddFromCSVForm(forms.Form):
    file = forms.FileField(
        label="", allow_empty_file=False, validators=[lambda x: validate_csv(x)]
    )
    spoj = forms.ChoiceField(
        label="Choose spoj",
        choices=get_choices(),
        widget=forms.Select(attrs={"style": "height: " "2.3612rem;"}),
    )

    # From DOCS: Don’t rely on validation of the file extension to determine a file’s type.
    # Files can be renamed to have any extension no matter what data they contain.
    # So it's just for preventing human error
    file.validators.append(
        FileExtensionValidator(
            allowed_extensions=["csv"], message="File must have .csv extension"
        )
    )
