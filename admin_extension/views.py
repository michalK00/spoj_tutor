import re

from django.db import transaction
from django.shortcuts import render, redirect
from .forms import AddFromCSVForm, choices, split_pattern, model_fields
from django.contrib.admin.views.decorators import staff_member_required

from tasks.models import Task


# Create your views here.
@staff_member_required()
def add_tasks_from_csv(request):
    def return_form():
        return render(request, "admin/add_tasks_csv.html", {"form": form, "model_fields": ", ".join(model_fields)})

    if request.method != "POST":
        form = AddFromCSVForm()
        return return_form()

    form = AddFromCSVForm(request.POST, request.FILES)
    if not form.is_valid():  # <- file is validated, so we can just use it as is
        return return_form()

    # Adding operation is one transaction
    with transaction.atomic():
        file = request.FILES.get("file")
        file.seek(0)

        lines = file.readlines()

        csv_fields = re.split(split_pattern, lines[0].decode().replace("\r\n", ""))
        csv_fields.append("spoj")

        for line in lines[1:]:
            fields = re.split(split_pattern, line.decode().replace("\r\n", '').replace('"', ''))
            fields.append(choices[int(form.cleaned_data["spoj"])][1])

            normalized_fields = [None if elem == "" else elem for elem in fields]

            data = dict(zip(csv_fields, normalized_fields))
            Task.objects.create(**data)
    return redirect("admin:index")
    # TODO: add file parsing, database modification and tests
