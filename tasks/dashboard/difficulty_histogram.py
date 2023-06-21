from collections import namedtuple

from tasks.models import UserTask


def get_histogram_data(request):
    solved_user_tasks = UserTask.objects.filter(user_id=request.user.id, finished_date__isnull=False).select_related(
        'task_id__spoj')
    unsolved_user_tasks = UserTask.objects.filter(user_id=request.user.id, finished_date__isnull=True).select_related(
        'task_id__spoj')

    Histogram = namedtuple("Histogram", ['solved_difficulty', 'unsolved_difficulty'])
    histogram = Histogram(solved_difficulty=calculate_difficulty(solved_user_tasks),
                          unsolved_difficulty=calculate_difficulty(unsolved_user_tasks))

    return histogram


def calculate_difficulty(user_task_list):
    tasks_list = []
    for user_task in user_task_list:
        spoj_difficulty_levels = user_task.task_id.spoj.amount_of_difficulty_levels
        task_difficulty = user_task.task_id.difficulty
        tasks_list.append(
            (task_difficulty + 1) / spoj_difficulty_levels
        )
    return tasks_list
