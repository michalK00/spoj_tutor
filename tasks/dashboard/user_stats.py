from collections import namedtuple

from tasks.models import UserTask, Task


def get_user_stats(request):
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
    return stats
