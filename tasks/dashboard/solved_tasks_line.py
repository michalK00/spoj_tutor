from tasks.models import UserTask


def get_line_data(request):
    solved_tasks_dates = UserTask.objects.all().filter(user_id=request.user.id,
                                                       finished_date__isnull=False).values_list(
        'finished_date', flat=True).order_by('finished_date')
    solved_tasks_dates = [f'{date.year}-{date.month}-{date.day}' for date in solved_tasks_dates]
    return solved_tasks_dates
