import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime

from .dashboard.difficulty_histogram import get_histogram_data
from .dashboard.solved_tasks_line import get_line_data
from .dashboard.tasks_pie import get_unsolved_pie, get_solved_pie
from .dashboard.user_stats import get_user_stats
from .forms import EditUserTask
from .models import Task, UserTask, Spoj
from .query_params.task_query_params import TaskQuery, UserTaskQuery


# Create your views here.
def tasks(request):
    if request.method == "POST":
        if "add-user-task" in request.POST:
            with transaction.atomic():
                task_id = request.POST["add-user-task"]
                task = Task.objects.get(id=task_id)
                UserTask(task_id=task, user_id=request.user).save()
        elif "delete-user-task" in request.POST:
            with transaction.atomic():
                task_id = request.POST["delete-user-task"]
                task = Task.objects.get(id=task_id)
                UserTask.objects.filter(task_id=task, user_id=request.user).delete()

    task_query = TaskQuery(request)
    task_list = task_query.filtered_queryset
    tasks_count = task_list.count()
    spojs = Spoj.objects.all()
    user_tasks_ids = []
    if request.user.id is not None:
        user_tasks_ids = UserTask.objects.filter(user_id=request.user.id).values_list('task_id', flat=True)
    queryset = task_list.order_by('title')
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'tasks/tasks.html',
                  {'tasks': tasks, 'spojs': spojs, 'task_query': task_query, "tasks_count": tasks_count,
                   "user_tasks_ids": user_tasks_ids})


def user_tasks(request):
    if request.method == "POST":
        with transaction.atomic():
            task_id = request.POST["delete-user-task"]
            task = UserTask.objects.get(id=task_id)
            task.delete()

    user_task_query = UserTaskQuery(request)
    task_list = user_task_query.filtered_queryset
    tasks_count = task_list.count()
    spojs = Spoj.objects.all()

    queryset = task_list.order_by('finished_date')
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
    return render(request, 'user_tasks/user_tasks.html',
                  {'tasks': tasks, 'spojs': spojs, 'task_query': user_task_query, "tasks_count": tasks_count})


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


def single_user_task(request, user_task_id):
    found_user_task = get_object_or_404(UserTask, pk=user_task_id)

    form = EditUserTask(request.POST,
                        initial={
                            "finished": found_user_task.finished_date,
                            "user_solution": found_user_task.user_solution,
                            "user_note": found_user_task.user_note
                        })

    def return_form():
        return render(request, 'user_tasks/user_task.html', {'form': form, 'user_task': found_user_task})

    if request.method != "POST":
        return return_form()

    if "solve" in request.POST:
        with transaction.atomic():
            user_task_id = request.POST["solve"]
            user_task = UserTask.objects.get(id=user_task_id)
            user_task.finished_date = datetime.now()
            user_task.save(update_fields=["finished_date"])
    elif "undo-solve" in request.POST:
        with transaction.atomic():
            user_task_id = request.POST["undo-solve"]
            user_task = UserTask.objects.get(id=user_task_id)
            user_task.finished_date = None
            user_task.save(update_fields=["finished_date"])
    else:
        with transaction.atomic():
            # Calling is valid so the form gets the data
            form.is_valid()
            user_task = get_object_or_404(UserTask, pk=user_task_id)
            user_task.user_note = form.cleaned_data["user_note"][2:-2]
            user_task.user_solution = form.cleaned_data["user_solution"][2:-2]
            user_task.save()

    return redirect("user_tasks")


def dashboard(request):
    context = {'stats': get_user_stats(request), 'solved_pie': get_solved_pie(request),
               'unsolved_pie': get_unsolved_pie(request),
               'histogram': get_histogram_data(request),
               'solved_tasks_dates': get_line_data(request)}

    return render(request, 'dashboard/dashboard.html', context)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
