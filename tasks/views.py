from .models import Task, Spoj
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .query_params.task_query_params import TaskQuery


# Create your views here.
def task(request):
    task_query = TaskQuery(request)
    task_list = task_query.task_list
    tasks_count = task_list.count()
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
        # in the url, so we fall back to the last page
        tasks = paginator.page(paginator.num_pages)
    print(task_query.params_count)
    return render(request, 'tasks/tasks.html', {'tasks': tasks, 'spojs': spojs, 'task_query': task_query, "tasks_count": tasks_count})



def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
