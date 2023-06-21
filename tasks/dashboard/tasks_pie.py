from collections import namedtuple

from django.db.models import Count, Case, When

from tasks.models import Spoj


def get_solved_pie(request):
    spoj_data = Spoj.objects.filter(task__user_tasks__user_id=request.user.id).annotate(
        num_solved=Count(Case(When(task__user_tasks__finished_date__isnull=False, then=1))))

    spoj_names = [spoj.name for spoj in spoj_data]
    num_user_tasks = [spoj.num_solved for spoj in spoj_data]
    SolvedPie = namedtuple("SolvedPie", ['num_user_tasks', 'spoj_names'])
    solved_pie = SolvedPie(num_user_tasks=num_user_tasks, spoj_names=spoj_names)

    return solved_pie


def get_unsolved_pie(request):
    spoj_data = Spoj.objects.filter(task__user_tasks__user_id=request.user.id).annotate(
        num_solved=Count(Case(When(task__user_tasks__finished_date__isnull=True, then=1))))

    spoj_names = [spoj.name for spoj in spoj_data]
    num_user_tasks = [spoj.num_solved for spoj in spoj_data]
    UnsolvedPie = namedtuple("UnsolvedPie", ['num_user_tasks', 'spoj_names'])
    unsolved_pie = UnsolvedPie(num_user_tasks=num_user_tasks, spoj_names=spoj_names)

    return unsolved_pie
