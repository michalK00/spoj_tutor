import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .forms import EditUserTask
from .models import Task, UserTask, Spoj
from .query_params.task_query_params import TaskQuery


# Create your views here.
def tasks(request):
    if request.method == "POST":
        if "add-user-task" in request.POST:
            task_id = request.POST["add-user-task"]
            task = Task.objects.get(id=task_id)
            UserTask(task_id=task, user_id=request.user).save()
        elif "delete-user-task" in request.POST:
            task_id = request.POST["delete-user-task"]
            task = Task.objects.get(id=task_id)
            UserTask.objects.filter(task_id=task, user_id=request.user).delete()

    task_query = TaskQuery(request)
    task_list = task_query.task_list
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
        # fallback to the first page
        tasks = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fall back to the last page
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'tasks/tasks.html',
                  {'tasks': tasks, 'spojs': spojs, 'task_query': task_query, "tasks_count": tasks_count,
                   "user_tasks_ids": user_tasks_ids})


class UserTaskListView(ListView):
    model = UserTask
    context_object_name = 'tasks'
    template_name = 'user_tasks/user_tasks.html'
    paginate_by = 20


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


# @method_decorator(login_required, name='dispatch')
# def single_user_task(request, user_task_id):
#     found_user_task = get_object_or_404(UserTask, pk=user_task_id)
#     return render(request, 'tasks/user_task.html', {'user_task': found_user_task})


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

    with transaction.atomic():
        # Calling is valid so the form gets the data
        form.is_valid()
        user_task = get_object_or_404(UserTask, pk=user_task_id)
        user_task.user_note = form.cleaned_data["user_note"][2:-2]
        user_task.user_solution = form.cleaned_data["user_solution"][2:-2]
        user_task.save()

    return redirect("user_tasks")


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
