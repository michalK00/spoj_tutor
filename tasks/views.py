import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .forms import EditUserTask
from .models import Task, UserTask


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



class UserTaskListView(ListView):
    model = UserTask
    context_object_name = 'user_tasks'
    template_name = 'tasks/user_tasks.html'
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
        return render(request, 'tasks/user_task.html', {'form': form, 'user_task': found_user_task})

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
