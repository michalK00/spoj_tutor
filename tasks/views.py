from .models import Task, Spoj
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# Create your views here.
def task(request):

    task_list = Task.objects.all()
    spojs = Spoj.objects.all()
    queryset = task_list.order_by('title')
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        tasks = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        tasks = paginator.page(paginator.num_pages)

    return render(request, 'tasks/tasks.html', {'tasks': tasks, 'spojs': spojs})


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
