import re

from django.db import transaction
from django.shortcuts import render, redirect

from utils import TaskRepresentation, get_amount_and_normalize_difficulty
from .forms import AddFromCSVForm, split_pattern, model_fields, get_choices
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

        tasks = []
        for line in lines[1:]:
            fields = re.split(split_pattern, line.decode().replace("\r\n", '').replace('"', ''))

            normalized_fields = [None if elem == "" else elem for elem in fields]

            data = dict(zip(csv_fields, normalized_fields))
            tasks.append(TaskRepresentation(**data))

        max_level = get_amount_and_normalize_difficulty(tasks)
        spoj = get_choices()[int(form.cleaned_data["spoj"])][1]

        if spoj.amount_of_difficulty_levels < max_level:
            spoj.amount_of_difficulty_levels = max_level
            spoj.save()

        for task in tasks:
            Task.objects.create(**(task.__dict__ | {"spoj": spoj}))

    return redirect("admin:index")