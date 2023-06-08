from .models import Task
from django.shortcuts import get_object_or_404, render


# Create your views here.
def tasks(request):
    all_tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': all_tasks})


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)



