from .models import Task, UserTask
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.db.models import Count


# Create your views here.
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/tasks.html'
    paginate_by = 20

    # def get_context_data(self, **kwargs):
    #     kwargs['task'] = self.task
    #     return super().get_context_data(**kwargs)
    #
    # def get_queryset(self):
    #     self.task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
    #     queryset = self.task.order_by('title').annotate(replies=Count('posts') - 1)
    #     return queryset


class UserTaskListView(ListView):
    model = UserTask
    context_object_name = 'user_tasks'
    template_name = 'tasks/user_tasks.html'
    paginate_by = 20


def single_task(request, task_id):
    found_task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task.html', {'task': found_task})


def single_user_task(request, user_task_id):
    found_user_task = get_object_or_404(UserTask, pk=user_task_id)
    return render(request, 'tasks/user_task.html', {'user_task': found_user_task})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
