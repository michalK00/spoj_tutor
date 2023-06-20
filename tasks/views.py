import datetime

import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from .forms import EditUserTask
from .models import Task, UserTask, Spoj
from .query_params.task_query_params import TaskQuery, UserTaskQuery
from django.db.models import Count, Case, When
from collections import namedtuple


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
    solved_no = UserTask.objects.filter(user_id=request.user.id, finished_date__isnull=False).count()
    saved_no = UserTask.objects.filter(user_id=request.user.id).count()
    total_no = Task.objects.all().count()

    Stats = namedtuple('Stats', ['solved_no', 'solved_ratio', 'saved_no', 'saved_ratio', 'total_no'])
    stats = Stats(
        solved_no=solved_no,
        saved_no=saved_no,
        total_no=total_no,
        solved_ratio="{:.2f}".format(solved_no / saved_no * 100),
        saved_ratio="{:.2f}".format(saved_no / total_no * 100)
    )

    spoj_data = Spoj.objects.filter(task__user_tasks__user_id=request.user.id).annotate(
        num_solved=Count(Case(When(task__user_tasks__finished_date__isnull=False, then=1))))

    spoj_names = [spoj.name for spoj in spoj_data]
    num_user_tasks = [spoj.num_solved for spoj in spoj_data]
    SolvedPie = namedtuple("SolvedPie", ['num_user_tasks', 'spoj_names'])
    solved_pie = SolvedPie(num_user_tasks=num_user_tasks, spoj_names=spoj_names)

    spoj_data = Spoj.objects.filter(task__user_tasks__user_id=request.user.id).annotate(
        num_solved=Count(Case(When(task__user_tasks__finished_date__isnull=True, then=1))))

    spoj_names = [spoj.name for spoj in spoj_data]
    num_user_tasks = [spoj.num_solved for spoj in spoj_data]
    UnsolvedPie = namedtuple("UnsolvedPie", ['num_user_tasks', 'spoj_names'])
    unsolved_pie = UnsolvedPie(num_user_tasks=num_user_tasks, spoj_names=spoj_names)

    solved_user_tasks = UserTask.objects.filter(user_id=request.user.id, finished_date__isnull=False).select_related(
        'task_id__spoj')
    unsolved_user_tasks = UserTask.objects.filter(user_id=request.user.id, finished_date__isnull=True).select_related(
        'task_id__spoj')

    def calculate_difficulty(user_task_list):
        tasks_list = []
        for user_task in user_task_list:
            spoj_difficulty_levels = user_task.task_id.spoj.amount_of_difficulty_levels
            task_difficulty = user_task.task_id.difficulty
            tasks_list.append(
                (task_difficulty + 1) / spoj_difficulty_levels
            )
        return tasks_list

    Histogram = namedtuple("Histogram", ['solved_difficulty', 'unsolved_difficulty'])
    histogram = Histogram(solved_difficulty=calculate_difficulty(solved_user_tasks),
                          unsolved_difficulty=calculate_difficulty(unsolved_user_tasks))

    solved_tasks_dates = UserTask.objects.all().filter(user_id=request.user.id, finished_date__isnull=False).values_list(
        'finished_date', flat=True).order_by('finished_date')
    solved_tasks_dates = [f'{date.year}-{date.month}-{date.day}' for date in solved_tasks_dates]
    print(solved_tasks_dates)
    return render(request, 'dashboard/dashboard.html',
                  {'stats': stats, 'solved_pie': solved_pie, 'unsolved_pie': unsolved_pie, 'histogram': histogram,
                   'solved_tasks_dates': solved_tasks_dates})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
