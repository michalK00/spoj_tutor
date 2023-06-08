from django.http import HttpResponse
from .models import Task, Spoj
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .forms import AddFromCSVForm
from spoj_tutor import urls


# Create your views here.
def tasks(request):
    all_tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': all_tasks})


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task.html', {'task': found_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def add_tasks_from_csv(request):
    if request.method == "POST":
        form = AddFromCSVForm(request.POST, request.FILES)
        if form.is_valid():

            # needs implementation
            return redirect('admin:index')
    else:
        form = AddFromCSVForm()
    # TODO: add file parsing, database modification and tests
    return render(request, 'add_tasks_csv.html', {'form': form})
