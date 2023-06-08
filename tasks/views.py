from django.http import HttpResponse
from .models import Task, Spoj
from django.shortcuts import get_object_or_404, render


# Create your views here.
def tasks(request):
    all_tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': all_tasks})


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task.html', {'task': found_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def spojs(request):
    all_spojs = Spoj.objects.all()
    return render(request, 'add_csv.html', {"spojs": all_spojs})


def add_records_from_csv(request):
    if request.method != "POST":
        return HttpResponse("Failure :c")
    # TODO: add file parsing, validation and database modification
    return HttpResponse(request.FILES.get("file_input"))
