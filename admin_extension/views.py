from django.db import transaction
from django.shortcuts import render, redirect
from .forms import AddFromCSVForm, choices
from django.contrib.admin.views.decorators import staff_member_required

from tasks.models import Task


# Create your views here.
@staff_member_required()
def add_tasks_from_csv(request):
    if request.method == "POST":
        form = AddFromCSVForm(request.POST, request.FILES)
        if form.is_valid():  # <- file is validated, so we can just use it as is
            # Adding operation is one transaction
            with transaction.atomic():
                file = request.FILES.get("file")
                file.seek(0)
                lines = file.readlines()
                csv_fields = lines[0].decode().strip().split(",")
                csv_fields.append("spoj")

                for line in lines[1:]:
                    fields = line.decode().replace("\r\n", "").split(",")

                    fields.append(choices[int(form.cleaned_data["spoj"])][1])

                    normalized_fields = [
                        None if elem == "" else elem for elem in fields
                    ]

                    data = dict(zip(csv_fields, normalized_fields))
                    Task.objects.create(**data)

            return redirect("admin:index")
    else:
        form = AddFromCSVForm()
    # TODO: add file parsing, database modification and tests
    return render(request, "admin/add_tasks_csv.html", {"form": form})
